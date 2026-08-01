
def test_edge_attributes(store_contraction_as):
    """Tests that node contraction preserves edge attributes."""
    # Shape: src1 --> dest <-- src2
    G = nx.DiGraph([("src1", "dest"), ("src2", "dest")])
    G["src1"]["dest"]["value"] = "src1-->dest"
    G["src2"]["dest"]["value"] = "src2-->dest"

    # New Shape: src1 --> dest
    H = nx.contracted_nodes(
        G, "src1", "src2", store_contraction_as=store_contraction_as
    )
    assert H.edges[("src1", "dest")]["value"] == "src1-->dest"  # Should be unchanged
    if store_contraction_as:
        assert (
            H.edges[("src1", "dest")][store_contraction_as][("src2", "dest")]["value"]
            == "src2-->dest"
        )
    else:
        assert store_contraction_as not in H.edges[("src1", "dest")]

    G = nx.MultiDiGraph(G)
    # New Shape: src1 -(x2)-> dest
    H = nx.contracted_nodes(
        G, "src1", "src2", store_contraction_as=store_contraction_as
    )
    # store_contraction should not affect multigraphs
    assert len(H.edges(("src1", "dest"))) == 2
    assert H.edges[("src1", "dest", 0)]["value"] == "src1-->dest"
    assert H.edges[("src1", "dest", 1)]["value"] == "src2-->dest"

