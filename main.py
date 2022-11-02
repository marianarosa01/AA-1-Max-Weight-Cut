#### Mariana Rosa,  98390 ####

import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from math import dist
from itertools import combinations, product
from numpy import save
from pyparsing import Or
from regex import P
import time
import pandas as pd



v = ["A", [9, 6]], ["B", [12, 14]], [
    "C", [15, 19]], ["D", [10, 19]], ["E", [19, 17]]
ed = [["C", "E"], ["A", "B"], ["C", "A"], ["C", "B"]]

def adjacency_list(edges):
    # {"vertices": [["A", [7, 6]], ["B", [3, 1]], ["C", [1, 13]], ["D", [12, 12]]],
    # "edges": [["C", "D"], ["A", "B"]]}

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

    #Exemplo de uma lista de adjacencias {'C': ['D'], 'D': ['C'], 'A': ['B'], 'B': ['A']}
    return adjacency_lst




def check_if_there_are_isolated_vertex(vertex,edges): #If there is any check isolated_vertex the problem is not solvable
    adj_list = adjacency_list(edges)
    vertex_in_adj_list = list(adj_list.keys())
    graph_vertex = [v for v,p in vertex]
    graph_vertex.sort()
    vertex_in_adj_list.sort()

    if graph_vertex == vertex_in_adj_list:
        return False #if there are none isolated vertex return False
    else:
        return True  #if there are isolated vertex return True



def calc(vertices, edges):  # Calculate the weight of the edges
    dic_edges_count = {} #Example of dic_edges_count {('A', 'B'): 1, ('C', 'D'): 5}
    for e1, e2 in edges:
        for v in vertices:
            if e1 == v[0][0]:
                point1 = v[1]
            if e2 == v[0][0]:
                point2 = v[1]
        dic_edges_count[e1, e2] = round(dist(point1, point2))

    return dic_edges_count

def calculate_weight_cut (subsetS, subsetT, weight_list): #Calculate the weight of the cut with the subsets S and T
    possible_edges = list(product(subsetS, subsetT))
    weight_sum = 0
    for edge in weight_list.keys():
        if edge in possible_edges or edge[::-1] in possible_edges:
            weight_sum += weight_list[edge]   
    return weight_sum

def find_max_cut_greedy(vertex, edges): #Greedy algorithm


    weights = calc(vertex, edges)
    sorted_weights = {edge: cost for edge, cost in sorted(weights.items(), key=lambda item: item[1], reverse=True)}

    #The heuristic used in these case was to find first the edges with the highest weight and put one vertex in subset S and another one in T

    subset_s = [list(sorted_weights.keys())[0][0]]
    subset_t = [list(sorted_weights.keys())[0][1]]
    iterations = 0
    # if there were only were one edge in the graph, the algorithm would not work, so we need to check if there is only one edge
    if len(sorted_weights) == 1:
        return  calculate_weight_cut(subset_s, subset_t, weights), subset_s, subset_t,0
    else:
        #then we will analyse the rest of the edges
        next_edges = list(sorted_weights.keys())[1:][0]
        #Example - next_edges = ('A', 'B')
        #If in the next edge, the vertex A is in subset S, we are going to put B in subset T, so they can be in different subsets to make the count of the cut
        if next_edges[0] in subset_s and next_edges[1] not in subset_t:
            subset_t.append(next_edges[1])

        #We can not only make this condition to evaluate this case, we need 3 more to make sure we evaluate all the cases

        elif next_edges[0] in subset_t and next_edges[1] not in subset_s:
            subset_s.append(next_edges[1])
        

        if next_edges[1] in subset_s and next_edges[0] not in subset_t:
            subset_t.append(next_edges[0])

        elif next_edges[1] in subset_t and next_edges[0] not in subset_s:
            subset_s.append(next_edges[0])
      

        final_vertices = list(sorted_weights.keys())[2:] # The rest of the vertices will go to subset T
        for v1,v2 in final_vertices:
            iterations +=1
            if v1 not in subset_t and not v1 in subset_s:
                subset_t.append(v1)
            if v2 not in subset_t and not v2 in subset_s:
                subset_t.append(v2)

        cut_weight = calculate_weight_cut(subset_s, subset_t, weights)
        return cut_weight, subset_s, subset_t,iterations


def plot_cut(vertices, edges, cuts,filepath,algorithm):
    #Plot the graph with the cut being the vertices in red the ones belonging to subset S and the ones in blue to subset T

    n_vertex = len(vertices)
    n_edges = len(edges)

    weight_edges = calc(vertices, edges)
    G = nx.Graph()

    color_map = []

    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=weight_edges[(edge[0], edge[1])])
    for node in range(len(vertices)):
        
        if vertices[node][0] in cuts:
            color_map.append('red')
            G.add_node(vertices[node][0], pos=vertices[node][1], color='red')
        else:
            color_map.append('blue')
            G.add_node(vertices[node][0], pos=vertices[node][1])

    labels = nx.get_edge_attributes(G, 'weight')
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw_networkx_edge_labels(G, pos, labels)
    nx.draw(G, pos, with_labels=True, node_color=color_map)
    if algorithm == "brute_force":
        plt.savefig(f"{filepath}/{n_vertex}vertices_{n_edges}_edges_brute.png", format="PNG")
        plt.close()

    elif algorithm == "greedy":
        plt.savefig(f"{filepath}/{n_vertex}vertices_{n_edges}_edges_greedy.png", format="PNG")
        plt.close()


def find_max_cut_brute_force(vertex, edges):
    #Brute force algorithm
    #We are going to find all the possible combinations of subsets S and T and then we are going to calculate the weight of the cut for each one of them
    #The combination with the highest weight will be the one we are going to return

    adj_list = adjacency_list(edges)
    weights = calc(vertex, edges)
    possible_cuts = []
    dic_cut_weight = {}
    iterations = 0
    graph_vertex = list(adj_list.keys())
    graph_vertex_number = len(list(adj_list.keys()))

    for i in range(1, int(graph_vertex_number/2)+1):
        combs = combinations(graph_vertex, i)
        if possible_cuts == []:
            possible_cuts = [','.join(comb) for comb in combs]
        else:
            possible_cuts = [','.join(comb) for comb in combs] + possible_cuts

    for cut in possible_cuts:
        iterations += 1
        chosen_cut = cut.split(',')
        subset_s = chosen_cut
        subset_t = [v for v in graph_vertex if v not in chosen_cut]
        weights_temp = weights.copy()
        cut_weight = calculate_weight_cut(subset_s, subset_t, weights_temp)
        dic_cut_weight[cut] = cut_weight
        

    max_cut_vertices = max(dic_cut_weight, key=dic_cut_weight.get)
    subset_s = list(max_cut_vertices.split(','))
    subset_t = list(set(graph_vertex) - set(subset_s))
    max_cut_value = dic_cut_weight[max_cut_vertices]

    return max_cut_value, subset_s, subset_t, iterations



def save_solution(vertex, edges, filepath):     #Save the solution in a txt file
    
    time_start_brute = time.time()
    name_file = "max_cut_"+str(len(vertex))+"_vertex_" + \
        str(len(edges))+"_edges"+".txt"
    adj_list = adjacency_list(edges)
    weights = calc(vertex, edges)
    if check_if_there_are_isolated_vertex(vertex, edges) == True:
        print("The problem is not solvable")
        with open(os.path.join(filepath, name_file), "w") as f:
            f.write("GRAPH WITH "+str(len(vertex))+" NODES \n\n")
            f.write(str(len(vertex)) + " vertices: " + str(vertex)+"\n")
            f.write(str(len(edges)) + " edges : " + str(edges)+"\n\n")
            f.write("Adjacency list: "+str(adj_list)+"\n")
            f.write("This problem is not solvable, it has isolated vertices.")
            f.close()
    else:

        #Brute force
        max_cut_brute = find_max_cut_brute_force(vertex, edges)
        time_end = time.time()
        execution_time_brute = str(time_end - time_start_brute)

        #Greedy
        time_start_greedy = time.time()
        max_cut_greedy = find_max_cut_greedy(vertex, edges)
        time_end_greedy = time.time()
        execution_time_greedy = str(time_end_greedy - time_start_greedy)
        

        with open(os.path.join(filepath, name_file), "w") as f:
            plot_cut(vertex, edges, max_cut_brute[1], filepath, "brute_force")
            plot_cut(vertex, edges, max_cut_greedy[1], filepath, "greedy")

            f.write("GRAPH WITH "+str(len(vertex))+" NODES \n\n")
            f.write(str(len(vertex)) + " vertices: "+str(vertex)+"\n")
            f.write(str(len(edges)) + " edges : "+str(edges)+"\n\n")
            f.write("Adjacency list: "+str(adj_list)+"\n")
            f.write("Weight list: "+str(weights)+"\n")

            f.write("WITH THE BRUTE FORCE ALGORITHM: \n")
            f.write("Maximum weight cut: " + str(max_cut_brute[0]) + "\n")
            f.write("Subset S: " + str(max_cut_brute[1]) + "\n")
            f.write("Subset T: " + str(max_cut_brute[2]) + "\n")
            f.write("NUMBER OF ITERATIONS: "+str(max_cut_brute[3])+"\n\n")
            f.write("TOTAL EXECUTION TIME: "+str(execution_time_brute)+"s \n\n")

            f.write("WITH THE GREEDY ALGORITHM: \n")
            f.write("Maximum weight cut: " + str(max_cut_greedy[0]) + "\n")
            f.write("Subset S: " + str(max_cut_greedy[1]) + "\n")
            f.write("Subset T: " + str(max_cut_greedy[2]) + "\n")
            f.write("NUMBER OF ITERATIONS: "+str(max_cut_greedy[3])+"\n\n")
            f.write("TOTAL EXECUTION TIME: "+execution_time_greedy+"s\n\n")


            f.close()


def plot_solutions_all():  #Plot all the solutions

    percentages = [12.5, 25, 50, 75]
    for p in percentages:
        path_percentage = "Percentage_" + str(p)
        path_solution = "solutions/"+path_percentage

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
                save_solution(vertex, edges, path_solution)
                jsons_data.loc[index] = [vertex, edges]


# plot_solutions_all() to generate all the files

"""
############################### Examples ########################################
# To run this code, you need to have the json files in the same folder as this code and just uncomment the lines you want to run and run the code.
# Example 1 (Brute force)
vertex = [["A", [20, 5]], ["B", [16, 2]], ["C", [16, 14]], ["D", [18, 6]], ["E", [11, 20]], ["F", [17, 3]], ["G", [19, 5]], ["H", [16, 2]]]
edges = [["B", "E"], ["G", "C"], ["C", "D"], ["A", "G"], ["G", "F"], ["B", "A"], ["B", "G"], ["F", "B"], ["B", "D"], ["F", "C"], ["E", "A"], ["E", "H"], ["A", "H"], ["H", "D"], ["D", "A"], ["C", "H"], ["E", "D"]]

results_brute = find_max_cut_brute_force(vertex, edges)
print("Maximum weight cut: ", results_brute[0])
print("Subset S: ", results_brute[1])
print("Subset T: ", results_brute[2])
print("Number of iterations: ", results_brute[3])


# Example 2 (Greedy)
results_greedy = find_max_cut_greedy(vertex, edges)
print("Maximum weight cut: ", results_greedy[0])
print("Subset S: ", results_greedy[1])
print("Subset T: ", results_greedy[2])
print("Number of iterations: ", results_greedy[3])

"""
