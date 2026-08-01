
def test_graph2():
    embedding_data = {
        0: [8, 6],
        1: [2, 6, 9],
        2: [8, 1, 7, 9, 6, 4],
        3: [9],
        4: [2],
        5: [6, 8],
        6: [9, 1, 0, 5, 2],
        7: [9, 2],
        8: [0, 2, 5],
        9: [1, 6, 2, 7, 3],
    }
    check_embedding_data(embedding_data)


def test_graph2():
    G = nx.Graph()
    G.add_edge("x", "a")
    G.add_edge("x", "b")
    G.add_edge("a", "c")
    G.add_edge("b", "c")
    G.add_edge("b", "d")
    G.add_edge("d", "e")
    G.add_edge("c", "y")
    G.add_edge("e", "y")
    _test_stoer_wagner(G, 2)

