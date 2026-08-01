
def test_weight_name():
    G = nx.cycle_graph(7)
    nx.set_edge_attributes(G, 1, "weight")
    nx.set_edge_attributes(G, 1, "foo")
    G.adj[1][2]["foo"] = 7
    paths = list(nx.shortest_simple_paths(G, 0, 3, weight="foo"))
    solution = [[0, 6, 5, 4, 3], [0, 1, 2, 3]]
    assert paths == solution


def test_weight_name():
    G = nx.Graph()
    G.add_edge(1, 2, weight=1, cost=8)
    G.add_edge(1, 3, cost=2)
    G.add_edge(2, 3, cost=4)
    _test_stoer_wagner(G, 6, weight="cost")

