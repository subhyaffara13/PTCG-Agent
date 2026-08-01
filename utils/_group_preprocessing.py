
def _group_preprocessing(G, set_v, weight):
    sigma = {}
    delta = {}
    D = {}
    betweenness = dict.fromkeys(G, 0)
    for s in G:
        if weight is None:  # use BFS
            S, P, sigma[s], D[s] = _single_source_shortest_path_basic(G, s)
        else:  # use Dijkstra's algorithm
            S, P, sigma[s], D[s] = _single_source_dijkstra_path_basic(G, s, weight)
        betweenness, delta[s] = _accumulate_endpoints(betweenness, S, P, sigma[s], s)
        for i in delta[s]:  # add the paths from s to i and rescale sigma
            if s != i:
                delta[s][i] += 1
            if weight is not None:
                sigma[s][i] = sigma[s][i] / 2
    # building the path betweenness matrix only for nodes that appear in the group
    PB = dict.fromkeys(G)
    for group_node1 in set_v:
        PB[group_node1] = dict.fromkeys(G, 0.0)
        for group_node2 in set_v:
            if group_node2 not in D[group_node1]:
                continue
            for node in G:
                # if node is connected to the two group nodes than continue
                if group_node2 in D[node] and group_node1 in D[node]:
                    if (
                        D[node][group_node2]
                        == D[node][group_node1] + D[group_node1][group_node2]
                    ):
                        PB[group_node1][group_node2] += (
                            delta[node][group_node2]
                            * sigma[node][group_node1]
                            * sigma[group_node1][group_node2]
                            / sigma[node][group_node2]
                        )
    return PB, sigma, D

