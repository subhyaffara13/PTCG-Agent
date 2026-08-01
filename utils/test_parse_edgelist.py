
def test_parse_edgelist():
    # ignore lines with less than 2 nodes
    lines = ["1;2", "2 3", "3 4"]
    G = nx.parse_edgelist(lines, nodetype=int)
    assert list(G.edges()) == [(2, 3), (3, 4)]
    # unknown nodetype
    with pytest.raises(TypeError, match="Failed to convert nodes"):
        lines = ["1 2", "2 3", "3 4"]
        nx.parse_edgelist(lines, nodetype="nope")
    # lines have invalid edge format
    with pytest.raises(TypeError, match="Failed to convert edge data"):
        lines = ["1 2 3", "2 3", "3 4"]
        nx.parse_edgelist(lines, nodetype=int)
    # edge data and data_keys not the same length
    with pytest.raises(IndexError, match="not the same length"):
        lines = ["1 2 3", "2 3 27", "3 4 3.0"]
        nx.parse_edgelist(
            lines, nodetype=int, data=(("weight", float), ("capacity", int))
        )
    # edge data can't be converted to edge type
    with pytest.raises(TypeError, match="Failed to convert"):
        lines = ["1 2 't1'", "2 3 't3'", "3 4 't3'"]
        nx.parse_edgelist(lines, nodetype=int, data=(("weight", float),))

