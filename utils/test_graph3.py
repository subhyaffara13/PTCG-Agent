
def test_graph3():
    # Source:
    # Stoer, M. and Wagner, F. (1997). "A simple min-cut algorithm". Journal of
    # the ACM 44 (4), 585-591.
    G = nx.Graph()
    G.add_edge(1, 2, weight=2)
    G.add_edge(1, 5, weight=3)
    G.add_edge(2, 3, weight=3)
    G.add_edge(2, 5, weight=2)
    G.add_edge(2, 6, weight=2)
    G.add_edge(3, 4, weight=4)
    G.add_edge(3, 7, weight=2)
    G.add_edge(4, 7, weight=2)
    G.add_edge(4, 8, weight=2)
    G.add_edge(5, 6, weight=3)
    G.add_edge(6, 7, weight=1)
    G.add_edge(7, 8, weight=3)
    _test_stoer_wagner(G, 4)

