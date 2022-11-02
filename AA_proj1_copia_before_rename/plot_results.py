import math
import os

import pandas as pd
import matplotlib.pyplot as plt

def read_results():
    # Dicionário para armazenar os resultados sendo a chave o nome do arquivo,
    # e o valor uma lista com os resultados [n, iteracoes, %edges, time]
    results_greedy = {}
    results_brute_force = {}

    results_dic = {} #being: {}
    percentages = [12.5, 25, 50, 75]
    for p in percentages:
        path_percentage = "Percentage_" + str(p)
        path_solution = "solutions/"+path_percentage


        results= [files for files in os.listdir(
            path_solution) if files.endswith('.txt')]

        for result in results:
            path_result = path_solution+"/"+result
            print(path_result)
            with open(path_result, "r") as f:
                lines = f.readlines()
                #BRUTE FORCE
                for line in lines[0:14]:
                    if "vertices" in line:
                        n = line[0]

                    if "NUMBER OF ITERATIONS:" in line:
                        n_it = line[21:].strip('\n')
                    
                    if "TOTAL EXECUTION TIME:" in line:
                            time = line[21:].strip('\n')
                            print(time)
                    
                results_brute_force[n] = [n_it, p, time]


                #GREEDY
                for line in lines[15:]:
                    if "vertices" in line:
                        n = line[0]

                    if "NUMBER OF ITERATIONS:" in line:
                        n_it = line[21:].strip('\n')
                    
                    if "TOTAL EXECUTION TIME:" in line:
                            time = line[21:].strip('\n')
                results_greedy [n] = [n_it, p, time]
        
        for k,v in results_greedy.items():
            print("GREEDY RESULTS: ", k, v)
        for k,v in results_brute_force.items():
            print("Brute force",k,v)
             

    return results_greedy, results_brute_force


def number_iterations():
    results_greedy, results_brute_force = read_results()
    #print(results_greedy)
    #print(results_brute_force)
    iterations_greedy = []
    iterations_brute_force = []
    percentages = [12.5, 25, 50, 75]
    for p in percentages:
        for k,v in results_greedy.items():
            if v[2] == p:
                iterations_greedy.append(v[1])
        for k,v in results_brute_force.items():
            if v[2] == p:
                iterations_brute_force.append(v[1])
    print(iterations_greedy)
    print(iterations_brute_force)

    x = results_greedy.keys()
    y = results_greedy.values()[0]
    plt.scatter(x, y, label="Greedy algorithm", color="blue",s=30)
    # x-axis label
    plt.xlabel('Graph Vertice Number of Graph Vertices (n)')
    plt.ylabel('Iterations')
    plt.title('Number of Iterations for Greedy')

    return iterations_greedy, iterations_brute_force
