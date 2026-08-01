
def test_bipartite_edgelist_consistent_strip_handling():
    """See gh-7462

    Input when printed looks like:

        A       B       interaction     2
        B       C       interaction     4
        C       A       interaction

    Note the trailing \\t in the last line, which indicates the existence of
    an empty data field.
    """
    lines = io.StringIO(
        "A\tB\tinteraction\t2\nB\tC\tinteraction\t4\nC\tA\tinteraction\t"
    )
    descr = [("type", str), ("weight", str)]
    # Should not raise
    G = nx.bipartite.parse_edgelist(lines, delimiter="\t", data=descr)
    expected = [("A", "B", "2"), ("A", "C", ""), ("B", "C", "4")]
    assert sorted(G.edges(data="weight")) == expected

