import cvxpy as cp
import numpy as np
#needs cvxopt, Mosek

def test_cases():
    n_paths = 4
    n_people = 15
    n_meetings = 2
    n_rooms =20

    E = np.random.randint(0, 2, (n_people, n_meetings))
    S = np.random.randint(0, 2, (n_people, n_rooms))
    D = np.random.randint(0,2,(n_paths, n_rooms, n_rooms))
    c = np.random.randint(0,4,(n_rooms,))

    E = np.zeros((n_people, n_meetings))
    E[0,0] = 1
    E[1,0] = 1
    E[2,0] = 1
    S = np.zeros((n_people, n_rooms))
    S[0:n_people, 0:n_people] = np.eye(n_people)

    return [E, S, D]

def validate_inputs(E, S, D):
    #E - matrix where rows are people, columns are meetings, indicates whether person is in meeting
    #S - matrix where rows are people, columns are rooms, indicates whether person starts in room
    #D - 3d matrix where depth [0] is path number, rows and columns are room, indicates whether path is included
    #    between rooms
    #return - list of errors, with corresponding numbers
    #   1 - multiple meetings per person
    #   2 - multiple starting rooms per person

    n_paths = D.shape[0]
    n_people = E.shape[0]
    n_meetings = E.shape[1]
    n_rooms = S.shape[1]

    meetpeoplefail = []
    roompeoplefail = []
    for i in range(n_people):
        meetcount = np.sum(E[i,:])
        roomcount = np.sum(S[i,:])
        if meetcount > 1:
            meetpeoplefail.append(i)
        if roomcount > 1:
            roompeoplefail.append(i)
    errors = []
    if len(meetpeoplefail) > 0:
        errors.append({"error": 1, "ids": meetpeoplefail})
    if len(roompeoplefail) > 0:
        errors.append({"error": 2, "ids": roompeoplefail})

    return errors


def optimize_assignments(E, S, D, c):
    #E - matrix where rows are people, columns are meetings, indicates whether person is in meeting
    #S - matrix where rows are people, columns are rooms, indicates whether person starts in room
    #D - 3d matrix where depth [0] is path number, rows and columns are room, indicates whether path is included
    #    between rooms
    #c - vector of room capacities


    n_paths = D.shape[0]
    n_people = E.shape[0]
    n_meetings = E.shape[1]
    n_rooms = S.shape[1]


    #Check meeting feasibility

    m_cap = cp.Variable((n_meetings, n_rooms), boolean = True)

    capacity_constraints = [1 == m_cap @ np.ones((n_rooms,)),
                   1 >= np.ones((n_meetings,)) @ m_cap,
                   c >= np.ones((n_people,)) @ (E @ m_cap)]

    capacity_obj = cp.Minimize(0)
    capacity_problem = cp.Problem(capacity_obj, capacity_constraints)
    capacity_problem.solve()

    if type(m_cap.value) == type(None):
        return {"error": 3, "expl": "Room capacities do not support meetings"}

    D_reshape = np.reshape(D, (n_paths, pow(n_rooms, 2)))

    x = cp.Variable(n_paths) #number of people on path
    p = cp.Variable((n_people, n_paths), integer=True) #indicator of whether person transverses path
    I = cp.Variable((n_people, pow(n_rooms, 2)), boolean = True) #indicator of whether person travels between rooms
    m = cp.Variable((n_meetings, n_rooms), boolean = True) #indicator of whether meeting is held in room
    m_long = cp.Variable((n_meetings, pow(n_rooms, 2)), boolean = True) #indicator of whether meeting is held in room - duplicated

    m_to_mlong = np.zeros((pow(n_rooms, 2), n_rooms))
    s_to_slong = np.zeros((pow(n_rooms, 2), n_rooms))
    for i in range(n_rooms):
        m_to_mlong[i*n_rooms:(i+1)*n_rooms,i] = 1
        s_to_slong[i*n_rooms:(i+1)*n_rooms,:] = np.eye(n_rooms)

    ##TODO
    slong = np.matmul(s_to_slong, S.T).T #check

    constraints = [x == np.ones((n_people,)) @ p, #x = sum p
                   1 == m @ np.ones((n_rooms,)), #one room for each meeting
                   1 >= np.ones((n_meetings,)) @ m, #at most one meeting for each room
                   p >= I @ D_reshape.T, #row person, column path, sum indicates whether person transverses path
                   m_long == (m_to_mlong @ m.T).T,#duplicates entries for each m
                   I >= (E @ m_long) + slong - 1, #check ##TODO
                   c >= np.ones((n_people,)) @ (E @ m)] #respect capacities

    objective = cp.Minimize(cp.sum_squares(x))
    problem = cp.Problem(objective, constraints)
    problem.solve()

    roomids = np.where(m.value >= .9)[1].tolist()

    meeting_score_denom = np.sum(E, 0)
    meeting_score_num = np.matmul((np.matmul(E.T, p.value)), np.square(x.value))
    meeting_score_denom[meeting_score_num==0] = 1

    meeting_score = np.divide(meeting_score_num, meeting_score_denom)

    return {"rooms": roomids, "scores": meeting_score}

#[E,S,D] = test_cases()
#print(validate_inputs(E, S, D))
#print(optimize_assignments(E, S, D, c))