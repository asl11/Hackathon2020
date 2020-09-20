import numpy as np
import pandas as pd
import networkx as nx
import optimize
import datetime

def load_data_old():

    person_df = pd.read_csv('PersonTable.csv', index_col='PersonID')
    # print(person_table['PersonID'])

    meeting_df = pd.read_csv('MeetingTable.csv', index_col='MeetingID')
    # print(meeting_df)

    location_df = pd.read_csv('LocationTable.csv', index_col='LocationID')

    graph_df = pd.read_csv('NetworkTable.csv')
    # print(graph_df)

    graph = nx.MultiGraph()
    # no_index_location_df = location_df.reset_index()
    network_G = nx.from_pandas_edgelist(graph_df, 'Node 1', 'Node 2', edge_attr='Edge_Weight', create_using=graph)

    return [person_df, meeting_df, location_df, graph_df, network_G]

def load_data():

    xls = pd.ExcelFile('./uploads/test_docs/HackRiceDataExcel.xlsx')

    person_df = pd.read_excel(xls, 'PersonTable')
    #person_df = person_df.set_index('PersonID')
    #print(person_df)

    meeting_df = pd.read_excel(xls, 'MeetingTable')
    meeting_df = meeting_df.set_index('MeetingID')

    location_df = pd.read_excel(xls, 'LocationTable')
    location_df = location_df.set_index('LocationID')

    graph_df = pd.read_excel(xls, 'NetworkTable')
    #print(graph_df)

    graph = nx.MultiGraph()
    #no_index_location_df = location_df.reset_index()
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

    for location1 in adjusted_location_df['LocationID']:
        for location2 in adjusted_location_df['LocationID']:
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
    for node in location_df.reset_index()['LocationID']:
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
        times.append(time.hour)
    return times

def run():

    [person_df, meeting_df, location_df, graph_df, network_G] = load_data()

    table_vals = [] #{"MeetingID", "MeetingTime", "AssignedRoom", "NumberofAttendees", "Score"}


    D = create_path_adjacency_matrix(location_df, graph_df, network_G)
    S_init = create_person_startroom_matrix(person_df, location_df)
    S = S_init
    E = create_person_meeting_matrix(person_df, meeting_df)
    c = load_capacities(location_df)
    times = np.asarray(load_times(meeting_df))
    time_start = min(times)
    time_end = max(times)


    for time in range(time_start, time_end + 1):
        print(time)
        meetids = np.where(times==time)[0]
        print(meetids)
        sub_ps = np.asarray(person_df[person_df["MeetingID"].isin(meetids)].index)

        if len(meetids) == 0:
            continue
        include_idx = np.isin(np.arange(E.shape[0]), sub_ps)

        subE1 = E[include_idx, :]
        subE = subE1[:, times == time]
        subS = S[include_idx, :]

        opt_out = optimize.optimize_assignments(subE, subS, D, c)
        assignments = opt_out["rooms"]
        scores = opt_out["scores"]

        #S_next = opt_out["end_locs"]
        #in_meeting = np.sum(S_next, 1)
        #S_small = S_next[include_idx]
        #S_next[in_meeting==0, :] = S_small[in_meeting==0, :]

        #S = S_next

        for i in range(len(assignments)):
            table_row = {"MeetingID": meeting_df["Meeting Name"][meetids[i]], "MeetingTime":str(time)+":00",
                         "AssignedRoom": location_df["LocationName"][assignments[i]],
                         "NumberofAttendees": int(np.sum(subE,0)[i]), "Score": float(round(scores[i], 2))}
            table_vals.append(table_row)

    return table_vals

