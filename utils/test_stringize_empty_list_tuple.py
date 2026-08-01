
def test_stringize_empty_list_tuple(coll):
    G = nx.path_graph(2)
    G.nodes[0]["test"] = coll  # test serializing an empty collection
    f = io.BytesIO()
    nx.write_gml(G, f)  # Smoke test - should not raise
    f.seek(0)
    H = nx.read_gml(f)
    assert H.nodes["0"]["test"] == coll  # Check empty list round-trips properly
    # Check full round-tripping. Note that nodes are loaded as strings by
    # default, so there needs to be some remapping prior to comparison
    H = nx.relabel_nodes(H, {"0": 0, "1": 1})
    assert nx.utils.graphs_equal(G, H)
    # Same as above, but use destringizer for node remapping. Should have no
    # effect on node attr
    f.seek(0)
    H = nx.read_gml(f, destringizer=int)
    assert nx.utils.graphs_equal(G, H)

