import numpy as np
import pandas as pd
import networkx as nx
import optimize
import datetime

def load_data():

    person_df = pd.read_csv('PersonTable.csv', index_col='PersonID')
    # print(person_table['PersonID'])

    meeting_df = pd.read_csv('MeetingTable.csv', index_col='MeetingID')
    # print(meeting_df)

    location_df = pd.read_csv('LocationTable.csv', index_col='Location ID')

    graph_df = pd.read_csv('NetworkTable.csv')
    # print(graph_df)

    graph = nx.MultiGraph()
    # no_index_location_df = location_df.reset_index()
    network_G = nx.from_pandas_edgelist(graph_df, 'Node 1', 'Node 2', edge_attr='Edge_Weight', create_using=graph)

    return [person_df, meeting_df, location_df, graph_df, network_G]

def create_location_network(location_df, graph_df, network_G):
    '''
    Makes network that connects locations to each other
    :return: Location Dataframe that has shortest paths with nodes
    '''

    count = 0
    # Possible Source of Error
    for index in range(len(graph_df)):
        graph_df.iloc[index]['EdgeID'] = count
        count += 1
    #print(graph_df)
    #print(nx.dijkstra_path(G, 'Old5', 'Commons'))

    shortest_path_df = pd.DataFrame(columns=['Source', 'Target', 'Path', 'PathLength'])

    adjusted_location_df = location_df.reset_index()

    #print(adjusted_location_df)

    for location1 in adjusted_location_df['Location ID']:
        for location2 in adjusted_location_df['Location ID']:
            nodes_shortest_path = nx.dijkstra_path(network_G, location1, #Find shortest path for each name
            location2)
            shortest_path_length = nx.shortest_path_length(network_G, location1, location2)
            new_row = {'Source': location1, 'Target': location2, 'Path': nodes_shortest_path, 'PathLength': shortest_path_length}
            shortest_path_df = shortest_path_df.append(new_row, ignore_index=True)
    return shortest_path_df

def create_path_adjacency_matrix(location_df, graph_df, network_G):
    '''
    First index: D[node_number, start_room, end_room]
    :return: 1 is included and 0 if not included
    '''
    shortest_path_graph = create_location_network(location_df, graph_df, network_G)
    n = len(location_df)
    #matrix_3d = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(n)]
    matrix_3d = np.zeros((n, n, n))
    for node in location_df.reset_index()['Location ID']:
        for edge in shortest_path_graph.iterrows():
            source = edge[1]['Source']
            target = edge[1]['Target']
            if node in edge[1]['Path']:
                matrix_3d[node][source][target] = 1
            else:
                matrix_3d[node][source][target] = 0
    return matrix_3d

def create_person_startroom_matrix(person_df, location_df):

    p = len(person_df)
    print(person_df)
    l = len(location_df)
    Srm = np.zeros((p, l))
    for i in range(p):
        prs = person_df.index[i]
        rm = person_df["PersonalRoomID"][i]
        Srm[prs, rm] = 1

    return Srm

def create_person_meeting_matrix(person_df, meeting_df):

    p = len(person_df)
    m = len(meeting_df)
    Pmt = np.zeros((p, m))
    for i in range(p):
        prs = person_df.index[i]
        mtg = person_df["MeetingID"][i]
        Pmt[prs, mtg] = 1

    return Pmt

def load_capacities(location_df):

    cap = location_df["Capacity"].to_numpy()
    return cap

def load_times(meeting_df):

    times_raw = meeting_df["Meeting Time"].to_numpy()
    times = []
    for time in times_raw:
        datetime_time = datetime.datetime.strptime(time, "%I:%M")
        times.append(datetime_time.hour)
    return times

def run():

    [person_df, meeting_df, location_df, graph_df, network_G] = load_data()


    table_vals = [] #{"MeetingID", "MeetingTime", "AssignedRoom", "NumberofAttendees", "Score"}


    D = create_path_adjacency_matrix(location_df, graph_df, network_G)
    S_init = create_person_startroom_matrix(person_df, location_df)
    S = S_init
    E = create_person_meeting_matrix(person_df, meeting_df)
    c = load_capacities(location_df)
    print(c)
    times = load_times(meeting_df)
    time_start = min(times)
    time_end = max(times)


    for time in range(time_start, time_end + 1):

        opt_out = optimize.optimize_assignments(E, S, D, c)
        assignments = opt_out["rooms"]
        scores = opt_out["scores"]


        S_next = opt_out["end_locs"]
        in_meeting = np.sum(S_next, 0)
        S_next[in_meeting==0, :] = S_init[in_meeting==0, :]

        S = S_next

        for i in range(len(assignments)):
            table_row = {"MeetingID": "", "AssignedRoom": assignments[i], "NumberofAttendees": "", "Score": scores[i]}
            table_vals.append(table_row)

    return table_row

run()