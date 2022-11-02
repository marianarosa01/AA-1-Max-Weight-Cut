
import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from math import dist
from itertools import combinations
import fnmatch
from numpy import save
from pyparsing import Or
from regex import P
import time
import pandas as pd
from collections import OrderedDict




v = ["A", [9, 6]], ["B", [12, 14]], [
    "C", [15, 19]], ["D", [10, 19]], ["E", [19, 17]]
ed = [["C", "E"], ["A", "B"], ["C", "A"], ["C", "B"]]

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

    # If there is any check isolated_vertex the problem is not solvable
def check_isolated_vertex(self, vertex, edges):
    adj_list = self.adjacency_list(edges)
    vertex_in_adj_list = list(adj_list.keys()).sort()
    print(vertex_in_adj_list)
    graph_vertex = [v for v in vertex].sort()
    if graph_vertex != vertex_in_adj_list:
        return True
    else:
        return False

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


def find_max_cut_greedy(vertex, edges):
    dic_cut_weight = {}
    weights = calc(vertex, edges)
    adj_list = adjacency_list(edges)
    print("the weights", weights)
    sorted_weights = {edge: cost for edge, cost in sorted(weights.items(), key=lambda item: item[1], reverse=True)}

    subset_s = [list(sorted_weights.keys())[0][0]]
    subset_t = [list(sorted_weights.keys())[0][1]]
    next_edges = list(sorted_weights.keys())[1:][0]
    if next_edges[0] not in subset_s and next_edges[0] in subset_t:
        subset_s.append(next_edges[1])
    if next_edges[1] not in subset_s and next_edges[1] not in subset_t:
        subset_s.append(next_edges[1])

    final_vertices = list(sorted_weights.keys())[2:]
    for v1,v2 in final_vertices:
        if v1 not in subset_t and not v1 in subset_s:
            subset_t.append(v1)
        if v2 not in subset_t and not v2 in subset_s:
            subset_t.append(v2)

    chosen_cut = subset_s

    weights_temp = weights.copy()
    print("chosen CUT", chosen_cut)
    if str(chosen_cut) in weights_temp.keys():
        print("Im here bitch")
    weights_temp.pop(str(chosen_cut[0]), str(chosen_cut[1]))
    print("weights_temp new", weights_temp)
    answer = 0
    for v in chosen_cut:
        print("v", v)
        neighbour = adj_list[v]
        print("neighbour", neighbour)
        for n in neighbour:
            edge = "('" + n + "', '" + v + "')"
            inverted_edge = "('" + v + "', '" + n + "')"
            print("edge", edge)

            for key in weights.keys():
                if str(key) == edge or str(key) == inverted_edge:
                    if key in weights_temp.keys():
                        print("ANSWER BEFORE", answer)
                        answer = weights[key] + answer
                        weights_temp.pop(key)
    print("final answer", answer)
    print("subset_s final", subset_s) # o corte que temos de fazer
    print("subset_t final", subset_t)

    return subset_s

find_max_cut_greedy(v, ed)

def plot_cut(vertices, edges, cuts):
    print("plotting")
    n_vertex = len(vertices)
    n_edges = len(edges)

    weight_edges = calc(vertices, edges)
    #print("these is vertices", vertices)
    G = nx.Graph()

    color_map = []

    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=weight_edges[(edge[0], edge[1])])
        #print("weight", weight_edges[(edge[0], edge[1])])
    for node in range(len(vertices)):
        ''' print("this is the node", node)
        print("this is the pos", vertices[node][1])
        print("O CORTE", cuts)
        print("O VERTICE", vertices[node][0]) '''
        if vertices[node][0] in cuts:
            color_map.append('red')
            G.add_node(vertices[node][0], pos=vertices[node][1], color='red')
        else:
            color_map.append('blue')
            G.add_node(vertices[node][0], pos=vertices[node][1])
        #print("pos", vertices[node][0], vertices[node][1])

    labels = nx.get_edge_attributes(G, 'weight')
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw_networkx_edge_labels(G, pos, labels)
    nx.draw(G, pos, with_labels=True, node_color=color_map)

    plt.savefig("graph.png")



def find_max_cut_brute_force(vertex, edges):

    adj_list = adjacency_list(edges)
    weights = calc(vertex, edges)
    possible_cuts = []
    dic_cut_weight = {}

    graph_vertex = list(adj_list.keys())
    graph_vertex_number = len(list(adj_list.keys()))

    for i in range(1, int(graph_vertex_number/2)+1):
        combs = combinations(graph_vertex, i)
        if possible_cuts == []:
            possible_cuts = [','.join(comb) for comb in combs]
        else:
            possible_cuts = [','.join(comb) for comb in combs] + possible_cuts

    for cut in possible_cuts:

        answer = 0
        chosen_cut = cut.split(',')
        weights_temp = weights.copy()
        for v in chosen_cut:
            neighbour = adj_list[v]
            for n in neighbour:
                edge = "('" + n + "', '" + v + "')"
                inverted_edge = "('" + v + "', '" + n + "')"
                for key in weights.keys():
                    if str(key) == edge or str(key) == inverted_edge:
                        if key in weights_temp.keys():
                            answer = weights[key] + answer
                            weights_temp.pop(key)
                            dic_cut_weight[cut] = answer

    max_cut_vertices = max(dic_cut_weight, key=dic_cut_weight.get)
    subset_s = list(max_cut_vertices.split(','))
    subset_t = list(set(graph_vertex) - set(subset_s))
    max_cut_value = dic_cut_weight[max_cut_vertices]
    print("this is brute force subset s", subset_s)
    print("this is brute force subset t", subset_t)

    return max_cut_value, subset_s, subset_t  
"""


def save_solution (vertex,edges,filepath):
    time_start = time.time()
    name_file= "greedy_solution.txt"
    adj_list = adjacency_list(edges)
    max_cut = find_max_cut_greedy(vertex,edges)
    time_end = time.time()
    execution_time = str(time_end - time_start)

    with open(os.path.join(filepath, name_file), "w") as f:
        #print("this is max_cut", max_cut)
        plot_cut(vertex,edges,max_cut)
        f.write("GRAPH WITH "+str(len(vertex))+" NODES \n\n")
        f.write("These are the " + str(len(vertex)) + " vertices: "+str(vertex)+"\n")
        f.write("These are the " + str(len(edges)) +" edges : "+str(edges)+"\n\n")
        f.write("WITH THE BRUTE FORCE ALGORITHM: \n")

        f.write("The maximum weight cut is "+str(max_cut[1])+" from the vertices " + str(max_cut[0])+ "\n")
        f.write("This is the adjacency list: "+str(adj_list)+"\n\n")
        f.write("TOTAL EXECUTION TIME: "+execution_time+"s\n")
        f.close()

save_solution(v,ed,"/home/mariana/Desktop/MEI_1sem/AA/greedy")
    # plot(v,ed)
    def save_solution(self, vertex, edges, filepath):
        time_start_brute = time.time()
        name_file = "max_cut_"+str(len(vertex))+"_vertex_" + \
            str(len(edges))+"_edges"+".txt"
        adj_list = self.adjacency_list(edges)
        if self.check_isolated_vertex(vertex, edges) == True:
            print("The problem is not solvable")
        else:
            #Brute force
            max_cut_brute = self.find_max_cut_brute_force(vertex, edges)
            time_end = time.time()
            execution_time_brute = str(time_end - time_start_brute)
            #Greedy
            time_start_greedy = time.time()
            max_cut_greedy = find_max_cut_greedy(vertex, edges)
            time_end_greedy = time.time()
            execution_time_greedy = str(time_end_greedy - time_start_greedy)
            with open(os.path.join(filepath, name_file), "w") as f:
                #print("this is max_cut", max_cut)
                self.plot_cut(vertex, edges, max_cut_brute[0], filepath)
                f.write("GRAPH WITH "+str(len(vertex))+" NODES \n\n")
                f.write(str(len(vertex)) +
                        " vertices: "+str(vertex)+"\n")
                f.write(+ str(len(edges)) +
                        " edges : "+str(edges)+"\n\n")
                f.write("Adjacency list: "+str(adj_list)+"\n")


                f.write("WITH THE BRUTE FORCE ALGORITHM: \n")
                f.write("Maximum weight cut: " + str(max_cut_brute[0]) + "\n")
                f.write("Subset S: " + str(max_cut_brute[1]) + "\n")
                f.write("Subset T: " + str(max_cut_brute[2]) + "\n")
                f.write("TOTAL EXECUTION TIME: "+execution_time_brute+" \n\n")
                
                f.write("WITH THE GREEDY ALGORITHM: \n")
                f.write("Maximum weight cut: " + str(max_cut_greedy[0]) + "\n")
                f.write("Subset S: " + str(max_cut_brute[1]) + "\n")
                f.write("Subset T: " + str(max_cut_brute[2]) + "\n")
                f.write("TOTAL EXECUTION TIME: "+execution_time_greedy+"s\n\n")


                f.close()


    def plot_solutions_all(self):

        percentages = [12.5, 25, 50, 75]
        for p in percentages:
            path_percentage = "Percentage_" + str(p)
            path_solution = "solutions/brute_force/"+path_percentage

            if os.path.exists(path_solution) == False:
                os.mkdir(path_solution)
            json_files = [pos_json for pos_json in os.listdir(
                path_percentage) if pos_json.endswith('.json')]
            jsons_data = pd.DataFrame(columns=['vertices', 'edges'])

            for index, js in enumerate(json_files):
                with open(os.path.join(path_percentage, js)) as json_file:
                    json_text = json.load(json_file)
                    vertex = json_text["vertices"]
                    edges = json_text["edges"]
                    self.save_solution(vertex, edges, path_solution)
                    jsons_data.loc[index] = [vertex, edges]


    def plot_solutions_50(self):

        path_percentage = "Percentage_50"
        path_solution = "solutions/brute_force/"+path_percentage

        if os.path.exists(path_solution) == False:
            os.mkdir(path_solution)
        json_files = [pos_json for pos_json in os.listdir(
            path_percentage) if pos_json.endswith('.json')]
        jsons_data = pd.DataFrame(columns=['vertices', 'edges'])

        for index, js in enumerate(json_files):
            with open(os.path.join(path_percentage, js)) as json_file:
                json_text = json.load(json_file)
                vertex = json_text["vertices"]
                edges = json_text["edges"]
                self.save_solution(vertex, edges, path_solution)
                jsons_data.loc[index] = [vertex, edges]


    # plot_solutions_50()
save_solution(v, ed, "solutions/brute_force/Percentage_50")

    """