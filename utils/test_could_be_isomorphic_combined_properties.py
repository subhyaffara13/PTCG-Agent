
def test_could_be_isomorphic_combined_properties(atlas_ids):
    """There are two pairs of graphs from the graph atlas that have the same
    combined degree-triangle distribution, but a different maximal clique
    distribution. See gh-7852."""
    G, H = (nx.graph_atlas(idx) for idx in atlas_ids)

    assert not nx.is_isomorphic(G, H)

    # Degree only
    assert nx.faster_could_be_isomorphic(G, H)
    assert nx.could_be_isomorphic(G, H, properties="d")
    # Degrees & triangles
    assert nx.fast_could_be_isomorphic(G, H)
    assert nx.could_be_isomorphic(G, H, properties="dt")
    # Full properties table (degrees, triangles, cliques)
    assert not nx.could_be_isomorphic(G, H)
    assert not nx.could_be_isomorphic(G, H, properties="dtc")
    # For these two cases, the clique distribution alone is enough to verify
    # the graphs can't be isomorphic
    assert not nx.could_be_isomorphic(G, H, properties="c")

