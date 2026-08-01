
def test_trophic_levels_singular_with_basal():
    """Should fail to compute if there are any parts of the graph which are not
    reachable from any basal node (with in-degree zero).
    """
    G = nx.DiGraph()
    # a has in-degree zero
    G.add_edge("a", "b")

    # b is one level above a, c and d
    G.add_edge("c", "b")
    G.add_edge("d", "b")

    # c and d form a loop, neither are reachable from a
    G.add_edge("c", "d")
    G.add_edge("d", "c")

    with pytest.raises(nx.NetworkXError) as e:
        nx.trophic_levels(G)
    msg = (
        "Trophic levels are only defined for graphs where every node "
        + "has a path from a basal node (basal nodes are nodes with no "
        + "incoming edges)."
    )
    assert msg in str(e.value)

    # if self-loops are allowed, smaller example:
    G = nx.DiGraph()
    G.add_edge("a", "b")  # a has in-degree zero
    G.add_edge("c", "b")  # b is one level above a and c
    G.add_edge("c", "c")  # c has a self-loop
    with pytest.raises(nx.NetworkXError) as e:
        nx.trophic_levels(G)
    msg = (
        "Trophic levels are only defined for graphs where every node "
        + "has a path from a basal node (basal nodes are nodes with no "
        + "incoming edges)."
    )
    assert msg in str(e.value)

