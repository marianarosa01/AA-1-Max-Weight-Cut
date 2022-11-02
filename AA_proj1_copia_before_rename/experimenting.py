

v =[["A", [9, 3]], ["B", [4, 6]], ["C", [14, 1]]]
ed=[["A", "C"]]

def adjacency_list(edges):
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



def check_if_there_are_isolated_vertex(vertex,edges): #If there is any check isolated_vertex the problem is not solvable
    adj_list = adjacency_list(edges)
    vertex_in_adj_list = list(adj_list.keys())
    print(vertex_in_adj_list)
    graph_vertex = [v for v,p in vertex]
    print(graph_vertex)
    graph_vertex.sort()
    vertex_in_adj_list.sort()

    if graph_vertex == vertex_in_adj_list:
        return False #if there are isolated vertex return True
    else:
        return True #if there are none isolated vertex return False

print(check_if_there_are_isolated_vertex(v,ed))