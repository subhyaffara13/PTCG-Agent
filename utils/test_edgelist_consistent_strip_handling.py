
def test_edgelist_consistent_strip_handling():
    """See gh-7462

    Input when printed looks like::

        1       2       3
        2       3
        3       4       3.0

    Note the trailing \\t after the `3` in the second row, indicating an empty
    data value.
    """
    s = io.StringIO("1\t2\t3\n2\t3\t\n3\t4\t3.0")
    G = nx.parse_edgelist(s, delimiter="\t", nodetype=int, data=[("value", str)])
    assert sorted(G.edges(data="value")) == [(1, 2, "3"), (2, 3, ""), (3, 4, "3.0")]

