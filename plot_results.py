import collections
import math
import os

import pandas as pd
import matplotlib.pyplot as plt


def read_results():
    # Dicionário para armazenar os resultados sendo a chave o nome do arquivo,
    # e o valor uma lista com os resultados [n, %edges]:[iteracoes, time, max_weight_cut]
    results_greedy = {}
    results_brute_force = {}

    results_dic = {}  # being: {}
    percentages = [12.5, 25, 50, 75]
    for p in percentages:
        path_percentage = "Percentage_" + str(p)
        path_solution = "solutions/"+path_percentage

        results = [files for files in os.listdir(
            path_solution) if files.endswith('.txt')]

        for result in results:
            path_result = path_solution+"/"+result
            with open(path_result, "r") as f:
                lines = f.readlines()
                # BRUTE FORCE
                n = int(lines[0][11:13].strip())
                for line in lines[0:14]:
                    if "NUMBER OF ITERATIONS:" in line:
                        n_it = int(line[22:].strip('\n'))

                    if "TOTAL EXECUTION TIME:" in line:
                        time = float(line[22:].replace('s', '').strip('\n'))

                    if "Maximum weight cut:" in line:
                        max_weight_cut = int(line[19:].strip('\n'))

                results_brute_force[n,p] = [n_it, time,max_weight_cut]
                # GREEDY
                for line in lines[15:]:
                    if "NUMBER OF ITERATIONS:" in line:
                        n_it = int(line[22:].strip('\n'))
                    if "TOTAL EXECUTION TIME:" in line:
                        time = float(line[22:].replace('s', '').strip('\n'))

                    if "Maximum weight cut:" in line:
                        max_weight_cut = int(line[19:].strip('\n'))

                results_greedy[n,p] = [n_it, time,max_weight_cut]
                f.close()

 


    return results_greedy, results_brute_force


def number_iterations():
    results_greedy, results_brute_force = read_results()
    print("RESULTS GREEDY", results_greedy)
    print("RESULTS BRUTE FORCE", results_brute_force)
    # print(results_greedy)
    # print(results_brute_force)
    list_iterations_result_greedy = [[x[0] for x in results_greedy.values()]]
    list_iterations_result_brute_force = [[x[0] for x in results_brute_force.values()]]

    number_vertices_greedy =[x[0] for x in results_greedy.keys()]
    number_vertices_brute_force =[x[0] for x in results_brute_force.keys()]
    # Greedy
    x = number_vertices_greedy
    y = list_iterations_result_greedy
    plt.scatter(x, y, label="Algoritmo de pesquisa gulosa", color="blue", s=30)
    # x-axis label
    plt.xlabel('Nº de vértices do grafo (n)')
    plt.ylabel('Nº iterações')
    plt.title('Nº de iterações pelo algoritmo de pesquisa gulosa')
    # showing legend
    plt.legend()
    plt.savefig('graficos/n_iteracoes_greedy.png')
    plt.show()
    
      # Brute force
    x = number_vertices_brute_force
    y = list_iterations_result_brute_force
    plt.scatter(x, y, label="Algoritmo de força bruta", color="red", s=30)
    # x-axis label
    plt.xlabel('Nº de vértices do grafo (n)')
    plt.ylabel('Nº iterações')
    plt.title('Nº de iterações pelo algoritmo de força bruta')
    plt.legend()
    plt.savefig('graficos/n_iteracoes_brute_force.png')
    plt.show()

    # Comparação entre os dois algoritmos
    x = number_vertices_greedy
    y = list_iterations_result_greedy
    plt.scatter(x, y, label="Algoritmo de pesquisa gulosa", color="blue", s=10)
    x = number_vertices_greedy
    y = list_iterations_result_brute_force
    plt.scatter(x, y, label="Algoritmo de força bruta", color="red", s=30)
    # x-axis label
    plt.xlabel('Nº de vértices do grafo (n)')
    plt.ylabel('Nº iterações')
    plt.title('Nº de iterações pelos algoritmos de pesquisa gulosa e força bruta')
    plt.legend()
    plt.savefig('graficos/n_iteracoes_comparacao.png')
    plt.show()




def execution_time():
    results_greedy, results_brute_force = read_results()

    list_time_result_greedy = [[x[1] for x in results_greedy.values()]]
    list_time_result_brute_force = [[x[1] for x in results_brute_force.values()]]
    number_vertices_greedy =[x[0] for x in results_greedy.keys()]
    number_vertices_brute_force =[x[0] for x in results_brute_force.keys()]


    # Greedy
    x = number_vertices_greedy
    y = list_time_result_greedy
    plt.scatter(x, y, label="Algoritmo de pesquisa gulosa", color="blue", s=30)
    # x-axis label
    plt.xlabel('Nº de vértices do grafo (n)')
    plt.ylabel('Tempo de execução (s)')
    plt.title('Tempo de execução pelo algoritmo de pesquisa gulosa')
    # showing legend
    plt.legend()
    plt.savefig('graficos/tempo_execucao_greedy.png')
    plt.show()

    # Brute force
    x = number_vertices_brute_force
    y = list_time_result_brute_force
    plt.scatter(x, y, label="Algoritmo de força bruta", color="red", s=30)
    # x-axis label
    plt.xlabel('Nº de vértices do grafo (n)')
    plt.ylabel('Tempo de execução (s)')
    plt.title('Tempo de execução pelo algoritmo de força bruta')
    plt.legend()
    plt.savefig('graficos/tempo_execucao_brute_force.png')
    plt.show()

    # Comparação entre os dois algoritmos
    x = number_vertices_greedy
    y = list_time_result_greedy
    plt.scatter(x, y, label="Algoritmo de pesquisa gulosa", color="blue", s=10)
    x = number_vertices_greedy
    y = list_time_result_brute_force
    plt.scatter(x, y, label="Algoritmo de força bruta", color="red", s=30)
    # x-axis label
    plt.xlabel('Nº de vértices do grafo (n)')
    plt.ylabel('Tempo de execução (s)')
    plt.title('Tempo de execução pelos algoritmos de pesquisa gulosa e força bruta')
    plt.legend()
    plt.savefig('graficos/tempo_execucao_comparacao.png')
    plt.show()

    pass


def weight_cut_results():
    results_greedy, results_brute_force = read_results()

    list_weight_result_greedy = [[x[2] for x in results_greedy.values()]]
    list_weight_result_brute_force = [[x[2] for x in results_brute_force.values()]]
    number_vertices_greedy =[x[0] for x in results_greedy.keys()]
    number_vertices_brute_force =[x[0] for x in results_brute_force.keys()]


    # Greedy
    x = number_vertices_greedy
    y = list_weight_result_greedy
    plt.scatter(x, y, label="Algoritmo de pesquisa gulosa", color="blue", s=30)
    # x-axis label
    plt.xlabel('Nº de vértices do grafo (n)')
    plt.ylabel('Peso máximo de corte')
    plt.title('Peso máximo de corte pelo algoritmo de pesquisa gulosa')
    # showing legend
    plt.legend()
    plt.savefig('graficos/tempo_execucao_greedy.png')
    plt.show()

    # Brute force
    x = number_vertices_brute_force
    y = list_weight_result_brute_force
    plt.scatter(x, y, label="Algoritmo de força bruta", color="red", s=30)
    # x-axis label
    plt.xlabel('Nº de vértices do grafo (n)')
    plt.ylabel('Peso máximo de corte')
    plt.title('Peso máximo de corte pelo algoritmo de força bruta')
    plt.legend()
    plt.savefig('graficos/tempo_execucao_brute_force.png')
    plt.show()

    # Comparação entre os dois algoritmos
    x = number_vertices_greedy
    y = list_weight_result_greedy
    plt.scatter(x, y, label="Algoritmo de pesquisa gulosa", color="blue", s=10)
    x = number_vertices_greedy
    y = list_weight_result_brute_force
    plt.scatter(x, y, label="Algoritmo de força bruta", color="red", s=30)
    # x-axis label
    plt.xlabel('Nº de vértices do grafo (n)')
    plt.ylabel('Peso máximo de corte (s)')
    plt.title('Peso máximo de corte pelos algoritmos de pesquisa gulosa e força bruta')
    plt.legend()
    plt.savefig('graficos/tempo_execucao_comparacao.png')
    plt.show()

weight_cut_results()

