import cvxpy as cp
import numpy as np

n_paths = 4
n_people = 15
n_meetings = 2
n_rooms =20

E = np.random.randint(0, 2, (n_people, n_meetings))
S = np.random.randint(0, 2, (n_people, n_rooms))
D = np.random.randint(0,2,(n_paths, n_rooms, n_rooms))




def optimize_assignments(E, S, D):
    #E - matrix where rows are people, columns are meetings, indicates whether person is in meeting
    #S - matrix where rows are people, columns are rooms, indicates whether person starts in room
    #D - 3d matrix where depth [0] is path number, rows and columns are room, indicates whether path is included
    #    between rooms

    n_paths = D.shape[0]
    n_people = E.shape[0]
    n_meetings = E.shape[1]
    n_rooms = S.shape[1]

    D_reshape = np.reshape(D, (n_paths, pow(n_rooms, 2)))

    x = cp.Variable(n_paths)
    p = cp.Variable((n_people, n_paths), integer=True)
    I = cp.Variable((n_people, pow(n_rooms, 2)), boolean = True)
    m = cp.Variable((n_meetings, n_rooms), boolean = True)
    m_long = cp.Variable((n_meetings, pow(n_rooms, 2)), boolean = True)

    m_to_mlong = np.zeros((pow(n_rooms, 2), n_rooms))
    s_to_slong = np.zeros((pow(n_rooms, 2), n_rooms))
    for i in range(n_rooms):
        m_to_mlong[i*n_rooms:(i+1)*n_rooms,i] = 1
        s_to_slong[i*n_rooms:(i+1)*n_rooms,:] = np.eye(n_rooms)

    ##TODO
    slong = np.matmul(s_to_slong, S.T).T #check
    print(slong)

    constraints = [x == np.ones((n_people,)) @ p, #x = sum p
                   1 == m @ np.ones((n_rooms,)), #one room for each meeting
                   1 >= np.ones((n_meetings,)) @ m, #at most one meeting for each room
                   p >= I @ D_reshape.T, #row person, column path, sum indicates whether person transverses path
                   m_long == (m_to_mlong @ m.T).T,#duplicates entries for each m
                   I >= (E @ m_long) + slong - 1] #check
    #ensure I_nm doesn't repeat for nm, mn

    objective = cp.Minimize(cp.sum_squares(x))
    problem = cp.Problem(objective, constraints)
    problem.solve()

    print(m.value)

    #for i in range(1,)
    #Aeq =
    #beq = np.

optimize_assignments(E, S, D)