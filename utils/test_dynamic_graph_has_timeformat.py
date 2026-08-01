
def test_dynamic_graph_has_timeformat(time_attr, dyn_attr, tmp_path):
    """Ensure that graphs which have a 'start' or 'stop' attribute get a
    'timeformat' attribute upon parsing. See gh-7914."""
    G = nx.MultiGraph(mode=dyn_attr)
    G.add_node(0)
    G.nodes[0][time_attr] = 1
    # Write out
    fname = tmp_path / "foo.gexf"
    nx.write_gexf(G, fname)
    # Check that timeformat is added to saved data
    with open(fname) as fh:
        assert 'timeformat="long"' in fh.read()
    # Round-trip
    H = nx.read_gexf(fname)
    # If any node has a "start" or "end" attr, it is considered dynamic
    # regardless of the graph "mode" attr
    assert H.graph["mode"] == "dynamic"
    assert nx.utils.nodes_equal(G.edges, H.edges)

