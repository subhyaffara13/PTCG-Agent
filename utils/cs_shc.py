
def cs_shc():
    graph = nx.Graph()
    graph.add_nodes_from([1, 2, 3, 4, 5])
    graph.add_edges_from([(1, 2), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (4, 5)])
    return graph

