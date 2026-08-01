
def test_directed_edge_swap(G):
    in_degree = set(G.in_degree)
    out_degree = set(G.out_degree)
    edges = set(G.edges)
    nx.directed_edge_swap(G, nswap=1, max_tries=100, seed=1)
    assert in_degree == set(G.in_degree)
    assert out_degree == set(G.out_degree)
    assert edges != set(G.edges)
    assert 3 == sum(e not in edges for e in G.edges)

