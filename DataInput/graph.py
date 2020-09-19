import networkx as nx
from pathlib import Path
import pandas as pd
import numpy as np
import scipy as sp

person_df = pd.read_csv('PersonTable.csv', index_col='PersonID')
#print(person_table['PersonID'])

meeting_df = pd.read_csv('MeetingTable.csv', index_col='MeetingID')
#print(meeting_table)

location_df = pd.read_csv('LocationTable.csv', index_col='Location ID')

graph_df = pd.read_csv('NetworkTable.csv')
#print(graph_df)

graph = nx.MultiGraph()
#no_index_location_df = location_df.reset_index()
network_G = nx.from_pandas_edgelist(graph_df, 'Node 1', 'Node 2', edge_attr='Edge_Weight', create_using=graph)

#TODO: make nodes numeric values so that adjacency matrix works, also fix ids
#TODO: maybe use the index parameter in the read_csv function
def create_location_network():
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

    print(adjusted_location_df)

    for location1 in adjusted_location_df['Location ID']:
        for location2 in adjusted_location_df['Location ID']:
            nodes_shortest_path = nx.dijkstra_path(network_G, location1, #Find shortest path for each name
            location2)
            shortest_path_length = nx.shortest_path_length(network_G, location1, location2)
            new_row = {'Source': location1, 'Target': location2, 'Path': nodes_shortest_path, 'PathLength': shortest_path_length}
            shortest_path_df = shortest_path_df.append(new_row, ignore_index=True)
    return shortest_path_df

def create_person_meeting_matrix():
    '''
    :return: person_meeting adjacency matrix
    '''
    #person_meeting_adjacency_matrix = np.adjace
    person_Graph = nx.DiGraph()
    adjusted_person_df = person_df.reset_index()
    Person_Meetings_G = nx.from_pandas_edgelist(adjusted_person_df, 'PersonID', 'MeetingID', create_using=person_Graph)

    Person_Meeting_Adjacency_Matrix = nx.to_numpy_matrix(Person_Meetings_G)
    return Person_Meeting_Adjacency_Matrix


def create_person_startroom_matrix():
    '''
    :return: person_startroom_matrix
    '''
    person_startroom_Graph = nx.DiGraph()
    adjusted_person_df = person_df.reset_index()
    Person_Startroom_G = nx.from_pandas_edgelist(adjusted_person_df, 'PersonID', 'PersonalRoomID', create_using=person_startroom_Graph)
    Person_Startroom_Adjacency_Matrix = nx.to_numpy_matrix(Person_Startroom_G)
    return Person_Startroom_Adjacency_Matrix, person_df


def create_path_adjacency_matrix():
    '''
    First index: D[node_number, start_room, end_room]
    :return: 1 is included and 0 if not included
    '''
    shortest_path_graph = create_location_network()
    n = len(location_df)
    matrix_3d = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for node in location_df.reset_index()['Location ID']:
        for edge in shortest_path_graph.iterrows():
            source = edge[1]['Source']
            target = edge[1]['Target']
            if node in edge[1]['Path']:
                matrix_3d[node][source][target] = 1
            else:
                matrix_3d[node][source][target] = 0
    return matrix_3d
    #for location in location_table.index:
        # For each edge, check

#print(create_person_meeting_matrix())
#print(create_person_startroom_matrix())
#print(create_location_network())
print(create_path_adjacency_matrix())

#print(create_person_startroom_matrix())



# Get list of edges
# Edge is one if edge is in between source and target, 0 otherwise

# Rows people, columns starting room

# TODO: Put these people in a data table and compare paths from different meetings

def createGraph(graph):
    Path("")

