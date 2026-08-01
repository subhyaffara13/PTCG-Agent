
def test_full_join_multigraph():
    # MultiGraphs
    G = nx.MultiGraph()
    G.add_node(0)
    G.add_edge(1, 2)
    H = nx.MultiGraph()
    H.add_edge(3, 4)

    U = nx.full_join(G, H)
    assert set(U) == set(G) | set(H)
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H)

    # MultiGraphs rename
    U = nx.full_join(G, H, rename=("g", "h"))
    assert set(U) == {"g0", "g1", "g2", "h3", "h4"}
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H)

    # MultiDiGraphs
    G = nx.MultiDiGraph()
    G.add_node(0)
    G.add_edge(1, 2)
    H = nx.MultiDiGraph()
    H.add_edge(3, 4)

    U = nx.full_join(G, H)
    assert set(U) == set(G) | set(H)
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H) * 2

    # MultiDiGraphs rename
    U = nx.full_join(G, H, rename=("g", "h"))
    assert set(U) == {"g0", "g1", "g2", "h3", "h4"}
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H) * 2

