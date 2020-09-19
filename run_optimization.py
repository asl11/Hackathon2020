import optimize

def run(E, S, D, c):

    table_vals = [] #{"Meeting ID", "Meeting Time", "Assigned Room", "Number of Attendees", "Score"}

    times = []
    time_start = min(times)
    time_end = max(times)

    for time in range(time_start, time_end + 1):
        subE = E[]

        opt_out = optimize.optimize_assignments(subE, S, D, c)
        assignments = opt_out["rooms"]
        scores = opt_out["scores"]

        for i in range(len(assignments)):
            table_row = {"Meeting ID": "", "Assigned Room": assignments[i], "Number of Attendees": "", "Score": scores[i]}
            table_vals.append(table_row)

    return table_row