
def test_full_join_graph():
    # Simple Graphs
    G = nx.Graph()
    G.add_node(0)
    G.add_edge(1, 2)
    H = nx.Graph()
    H.add_edge(3, 4)

    U = nx.full_join(G, H)
    assert set(U) == set(G) | set(H)
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H)

    # Rename
    U = nx.full_join(G, H, rename=("g", "h"))
    assert set(U) == {"g0", "g1", "g2", "h3", "h4"}
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H)

    # Rename graphs with string-like nodes
    G = nx.Graph()
    G.add_node("a")
    G.add_edge("b", "c")
    H = nx.Graph()
    H.add_edge("d", "e")

    U = nx.full_join(G, H, rename=("g", "h"))
    assert set(U) == {"ga", "gb", "gc", "hd", "he"}
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H)

    # DiGraphs
    G = nx.DiGraph()
    G.add_node(0)
    G.add_edge(1, 2)
    H = nx.DiGraph()
    H.add_edge(3, 4)

    U = nx.full_join(G, H)
    assert set(U) == set(G) | set(H)
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H) * 2

    # DiGraphs Rename
    U = nx.full_join(G, H, rename=("g", "h"))
    assert set(U) == {"g0", "g1", "g2", "h3", "h4"}
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H) * 2

