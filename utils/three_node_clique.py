
def three_node_clique():
    graph = nx.Graph()
    graph.add_nodes_from([1, 2, 3])
    graph.add_edges_from([(1, 2), (1, 3), (2, 3)])
    graph.nodes[1]["weight"] = 10
    graph.nodes[2]["weight"] = 20
    graph.nodes[3]["weight"] = 5
    return graph


def three_node_clique():
    graph = nx.Graph()
    graph.add_nodes_from([1, 2, 3])
    graph.add_edges_from([(1, 2), (1, 3), (2, 3)])
    return graph

