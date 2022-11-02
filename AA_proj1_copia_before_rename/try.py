from itertools import combinations, product
from math import dist
import numpy as np

def adjancy_list(edges):
    # {"vertices": [["A", [7, 6]], ["B", [3, 1]], ["C", [1, 13]], ["D", [12, 12]]],
    # "edges": [["C", "D"], ["A", "B"]]}

    # Primeiro é preciso ver a nossa lista de adjacências, ou seja, que vértices estão ligados pelas arestas
    adjacency_lst = {}
    for v1, v2 in edges:
        if v1 in adjacency_lst:
            adjacency_lst[v1].append(v2)
        else:
            adjacency_lst[v1] = [v2]
        if v2 in adjacency_lst:
            adjacency_lst[v2].append(v1)
        else:
            adjacency_lst[v2] = [v1]

    #{'C': ['D'], 'D': ['C'], 'A': ['B'], 'B': ['A']}
    return adjacency_lst
    
def calc(vertices, edges):  # calcular o peso das arestas
    dic_edges_count = {}

    for e1, e2 in edges:
        for v in vertices:
            if e1 == v[0][0]:
                point1 = v[1]

            if e2 == v[0][0]:
                point2 = v[1]

        dic_edges_count[e1, e2] = round(dist(point1, point2))

    return dic_edges_count




##Build  weights
#dic = {[A,B], peso}
    




v = [['A', [3, 4]], ['B', [9, 1]], ['C', [4, 13]], ['D', [9, 19]], ['E', [18, 19]], ['F', [5, 9]], ['G', [15, 6]], ['H', [9, 4]], ['I', [16, 12]], ['J', [4, 3]], ['K', [6, 15]], ['L', [6, 10]], ['M', [14, 14]], ['N', [11, 15]], ['O', [8, 9]], ['P', [14, 10]], ['Q', [8, 14]]]
ed =  [['A', 'M'], ['I', 'K'], ['P', 'H'], ['A', 'N'], ['A', 'K'], ['E', 'G'], ['N', 'P'], ['M', 'B'], ['O', 'B'], ['E', 'J'], ['Q', 'B'], ['J', 'G'], ['F', 'E'], ['A', 'F'], ['D', 'F'], ['O', 'F'], ['O', 'J'], ['G', 'H'], ['D', 'Q'], ['G', 'P'], ['L', 'N'], ['M', 'F'], ['N', 'F'], ['C', 'N'], ['Q', 'F'], ['K', 'N'], ['I', 'A'], ['D', 'A'], ['N', 'M'], ['P', 'C'], ['E', 'K'], ['J', 'N'], ['Q', 'C'], ['P', 'E'], ['D', 'C'], ['A', 'Q'], ['K', 'P'], ['O', 'K'], ['J', 'H'], ['H', 'N'], ['H', 'M'], ['P', 'J'], ['K', 'G'], ['C', 'L'], ['A', 'C'], ['F', 'B'], ['I', 'M'], ['G', 'M'], ['L', 'K'], ['J', 'F'], ['L', 'G'], ['B', 'J'], ['E', 'O'], ['P', 'O'], ['G', 'C'], ['G', 'I'], ['P', 'A'], ['K', 'J'], ['O', 'A'], ['M', 'K'], ['Q', 'L'], ['O', 'Q'], ['I', 'C'], ['H', 'D'], ['J', 'Q'], ['F', 'L'], ['K', 'B'], ['B', 'A'], ['L', 'M'], ['M', 'J'], ['B', 'L'], ['G', 'A'], ['B', 'C'], ['H', 'F'], ['A', 'J'], ['O', 'N'], ['P', 'B'], ['P', 'M'], ['L', 'J'], ['H', 'B'], ['M', 'D'], ['H', 'Q'], ['H', 'I'], ['O', 'I'], ['O', 'G'], ['K', 'F'], ['B', 'N'], ['N', 'D'], ['C', 'O'], ['E', 'A']]
def check_isolated_vertex(vertex,edges): #If there is any check isolated_vertex the problem is not solvable
    adj_list = adjancy_list(edges)
    vertex_in_adj_list = list(adj_list.keys())
    print(vertex_in_adj_list)
    graph_vertex = [v for v in vertex]

    if graph_vertex.sort() != vertex_in_adj_list.sort():
        return True
    else:
        return False

print("check isolated", check_isolated_vertex(v, ed))

def calculate_weight_cut (subsetS, subsetT, weight_list):
    print("weight list", weight_list)
    possible_edges = list(product(subsetS, subsetT))
    print("possible edges", possible_edges)
    weight_sum = 0
    for edge in weight_list.keys():
        if edge in possible_edges or edge[::-1] in possible_edges:
            print("Edge", edge)
            print("Edge -1", edge[::-1])

            weight_sum += weight_list[edge]

   
    print("final weight", weight_sum)
    return weight_sum

weights = calc(v, ed)

sorted_weights = {edge: cost for edge, cost in sorted(weights.items(), key=lambda item: item[1], reverse=True)}

print("weight list", sorted_weights)