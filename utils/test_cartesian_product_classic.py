
def test_cartesian_product_classic():
    # test some classic product graphs
    P2 = nx.path_graph(2)
    P3 = nx.path_graph(3)
    # cube = 2-path X 2-path
    G = nx.cartesian_product(P2, P2)
    G = nx.cartesian_product(P2, G)
    assert nx.is_isomorphic(G, nx.cubical_graph())

    # 3x3 grid
    G = nx.cartesian_product(P3, P3)
    assert nx.is_isomorphic(G, nx.grid_2d_graph(3, 3))

