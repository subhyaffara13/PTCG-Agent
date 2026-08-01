
def disconnected():
    graph = nx.Graph()
    graph.add_edges_from([(1, 2), (2, 3), (4, 5), (5, 6)])
    graph.nodes[1]["weight"] = 10
    graph.nodes[2]["weight"] = 20
    graph.nodes[3]["weight"] = 5
    graph.nodes[4]["weight"] = 100
    graph.nodes[5]["weight"] = 200
    graph.nodes[6]["weight"] = 50
    return graph


def disconnected():
    graph = nx.Graph()
    graph.add_edges_from([(1, 2), (2, 3), (4, 5), (5, 6)])
    return graph

