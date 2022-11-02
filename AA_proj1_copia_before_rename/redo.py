import networkx as nx
import matplotlib.pyplot as plt
from math import dist
from itertools import combinations


def adjacency_list(vertices,edges):
    letters_vertex = [v[0] for v in vertices] 
    G = nx.Graph()
    G = nx.DiGraph()
    G.add_nodes_from(letters_vertex)
    G.add_edges_from(edges)

    list  = nx.write_adjlist(G, "adjacency_list.txt")

    return nx.read_adjlist("adjacency_list.txt")



def show_graph(vertices,edges):
    letters_vertex = [v[0] for v in vertices] 

    print("this are the letters",letters_vertex)
    G = nx.Graph()
    G.add_nodes_from([0, len(vertices)-1])
    for edge in edges:
        G.add_edge(letters_vertex.index(edge[0]),letters_vertex.index(edge[1]))
    nx.draw(G, with_labels=True)
    plt.show()

v = ["A", [9, 6]], ["B", [12, 14]], ["C", [15, 19]], ["D", [10, 19]], ["E", [19, 17]]
ed = [["C", "E"], ["A", "B"], ["C", "A"], ["C", "B"]]

print(adjacency_list(v,ed))

#isto funciona
def plot(vertices,edges):
    weight_edges = calc(vertices,edges)
    print("these is vertices", vertices)
    G = nx.Graph()

    for edge in edges:
        G.add_edge(edge[0],edge[1], weight=weight_edges[(edge[0],edge[1])])
        print("weight", weight_edges[(edge[0],edge[1])])
    for node in range(len(vertices)):
        print("this is the node", node)
        print("this is the pos", vertices[node][1])
        G.add_node(vertices[node][0], pos=vertices[node][1])
        print("pos",vertices[node][0],vertices[node][1])
    
    labels = nx.get_edge_attributes(G,'weight')
    pos = nx.get_node_attributes(G,'pos')
    nx.draw_networkx_edge_labels(G, pos, labels)
    nx.draw(G, pos, with_labels=True)
    plt.show()

