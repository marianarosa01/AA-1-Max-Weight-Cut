from graph_analysys import GraphAnalysys

v = ["A", [9, 6]], ["B", [12, 14]], ["C", [15, 19]], ["D", [10, 19]], ["E", [19, 17]]
ed = [["C", "E"], ["A", "B"], ["C", "A"], ["C", "B"]]


class GreedySearch:

    def __init__(self):
        self.find_max_cut_greedy(self,v, ed)

    def find_max_cut_greedy(self, vertex, edges):
        answer = 0
        weights = GraphAnalysys.calc(self,vertex, edges)
        adj_list = GraphAnalysys.adjacency_list(edges)
        dic_cut_weight = {}

        print("the weights", weights)
        sorted_weights = {edge: cost for edge, cost in sorted(
            weights.items(), key=lambda item: item[1], reverse=True)}
        print("sorted", sorted_weights)

        subset_s = [list(sorted_weights.keys())[0][0]]
        print("subset_s primeira", subset_s)
        subset_t = [list(sorted_weights.keys())[0][1]]
        print("subset_t primeira", subset_t)
        next_edges = list(sorted_weights.keys())[1:][0]
        print("next edge to analyse", next_edges)
        if next_edges[0] not in subset_s and next_edges[0] in subset_t:
            subset_s.append(next_edges[1])
        if next_edges[1] not in subset_s and next_edges[1] not in subset_t:
            subset_s.append(next_edges[1])

        final_vertices = list(sorted_weights.keys())[2:]
        for v1, v2 in final_vertices:
            if v1 not in subset_t and not v1 in subset_s:
                subset_t.append(v1)
            if v2 not in subset_t and not v2 in subset_s:
                subset_t.append(v2)

            chosen_cut = subset_s
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
                                dic_cut_weight[chosen_cut] = answer
        print(answer)
        print("subset_s final", subset_s)  # o corte que temos de fazer
        print("subset_t final", subset_t)

        return subset_s, subset_t

