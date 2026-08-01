
def test_margulis_gabber_galil_graph_properties(n):
    g = nx.margulis_gabber_galil_graph(n)
    assert g.number_of_nodes() == n * n
    for node in g:
        assert g.degree(node) == 8
        assert len(node) == 2
        for i in node:
            assert int(i) == i
            assert 0 <= i < n

