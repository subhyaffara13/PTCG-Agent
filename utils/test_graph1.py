
def test_graph1():
    embedding_data = {0: [1, 2, 3], 1: [2, 0], 2: [3, 0, 1], 3: [2, 0]}
    check_embedding_data(embedding_data)


def test_graph1():
    G = nx.Graph()
    G.add_edge("x", "a", weight=3)
    G.add_edge("x", "b", weight=1)
    G.add_edge("a", "c", weight=3)
    G.add_edge("b", "c", weight=5)
    G.add_edge("b", "d", weight=4)
    G.add_edge("d", "e", weight=2)
    G.add_edge("c", "y", weight=2)
    G.add_edge("e", "y", weight=3)
    _test_stoer_wagner(G, 4)

