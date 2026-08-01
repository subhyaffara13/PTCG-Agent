
def test_AS_graph_coverage():
    """Add test coverage for some hard-to-hit branches."""
    GG = AS_graph_generator(20, seed=42)
    G = GG.generate()
    assert len(G) == 20

    # Proportion of M nodes is 0.15, so there are 3 when n = 20.
    assert len(GG.nodes["M"]) == 3
    m_node = nx.utils.arbitrary_element(GG.nodes["M"])
    # Proportion of CP nodes is 0.05, so there is 1 when n = 20.
    assert len(GG.nodes["CP"]) == 1
    cp_node = nx.utils.arbitrary_element(GG.nodes["CP"])

    # All M nodes are already connected to each other.
    assert all(u in G[v] for u in GG.nodes["M"] for v in GG.nodes["M"] if u != v)

    # Add coverage for the unsuccessful branches when adding peering links.
    # `add_m_peering_link` cannot add edges when the nodes are already connected.
    assert not GG.add_m_peering_link(m_node, "M")
    # Artificially add nodes to `customers` to check customer neighbors are
    # correctly excluded.
    GG.customers[m_node] = set(GG.nodes["M"])
    assert not GG.add_m_peering_link(m_node, "M")

    # Artificially remove nodes from `providers` to check neighbors are
    # correctly excluded (otherwise they might already get disqualified).
    GG.providers[cp_node] = set()
    assert not GG.add_cp_peering_link(cp_node, "CP")
    assert not GG.add_cp_peering_link(cp_node, "M")

    # Add coverage for trying to add a new M node where one already exists.
    GG.add_node(m_node, "M", 1, 2, 0.5)
    assert len(GG.nodes["M"]) == 3

