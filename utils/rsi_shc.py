
def rsi_shc():
    graph = nx.Graph()
    graph.add_nodes_from([1, 2, 3, 4, 5, 6])
    graph.add_edges_from(
        [(1, 2), (1, 5), (1, 6), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6)]
    )
    return graph

