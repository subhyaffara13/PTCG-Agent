
def test_margulis_gabber_galil_graph_eigvals(n):
    np = pytest.importorskip("numpy")
    sp = pytest.importorskip("scipy")

    g = nx.margulis_gabber_galil_graph(n)
    # Eigenvalues are already sorted using the scipy eigvalsh,
    # but the implementation in numpy does not guarantee order.
    w = sorted(sp.linalg.eigvalsh(nx.adjacency_matrix(g).toarray()))
    assert w[-2] < 5 * np.sqrt(2)

