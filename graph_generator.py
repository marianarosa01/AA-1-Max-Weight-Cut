# Mariana Rosa, 98390

import random
import json
import matplotlib.pyplot as plt
import os.path

random.seed(98390)

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
            'T', 'U', 'V', 'W', 'X', 'Y', 'Z']  # Vertices will be the letters of the alphabet


##GENERATE GRAPH!

def graph_generator(n, p):  # n = number of vertices, p = percentage of edges
    edges = []
    vertices = []

    #N must be between 0 and the length of our list of possible vertices
    if 0 < n < len(alphabet):
        for i in range(n):  # Generate vertices
            coordinates = []
            x = random.randint(1, 20)
            y = random.randint(1, 20)
            if ((x, y) in coordinates) == False:
                coordinates.append((x, y))
            # example: [ ['A', (3,2)], ['B', (1,5)], ...]
            vertices.append([alphabet[i], (x, y)])

    min_arestas = n-1
    print("Nº mínimo de arestas", min_arestas)
    max_arestas = int(n*(n-1)/2)
    print("Nº máximo de arestas", max_arestas)

    if n > 2:
        num_arestas = int(p/100 * max_arestas)
        print("Nº de arestas", num_arestas)
    else:
        print("sou estranho")
        num_arestas = 1

    vertices_with_edges = set()

    # Build edges

    if min_arestas <= num_arestas <= max_arestas:
        for i in range(num_arestas):
            while True:
                v1 = random.choice(vertices)[0]
                v2 = random.choice(vertices)[0]
                if v1 != v2:
                    if (v1, v2) not in edges and (v2, v1) not in edges:
                        edges.append((v1, v2))
                        break
                    if len(vertices) != len(vertices_with_edges):  # Para o grafo ser conexo
                        if v1 not in vertices_with_edges or v2 not in vertices_with_edges:
                            vertices_with_edges.update({v1, v2})
                            if ((v1, v2) in edges == False) and ((v2, v1) in edges) == False:
                                edges.append((v1, v2))
                            break
    return vertices, edges


print(graph_generator(5, 50))


def create_graphs_files():
    percentages = [12.5, 25, 50, 75]

    for p in percentages:
        path_percentage = "Percentage_" + str(p)
        if os.path.exists(path_percentage) == False:
            os.mkdir(path_percentage)
            for i in range(len(alphabet)):  # 2 to 24 vertices, alfabeto
                v, e = graph_generator(i, p)
                if len(e):
                    with open(path_percentage + "/graph_with_" + str(i) + "_vertices_" + str(p) + ".json", "w") as f:
                        json.dump({"vertices": v , "edges": e}, f)

        
create_graphs_files()