
def test_is_separating_set():
    for i in [5, 10, 15]:
        G = nx.star_graph(i)
        max_degree_node = max(G, key=G.degree)
        assert _is_separating_set(G, {max_degree_node})

