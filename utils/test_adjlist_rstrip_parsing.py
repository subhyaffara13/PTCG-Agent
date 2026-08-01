
def test_adjlist_rstrip_parsing(lines, delim):
    """Regression test related to gh-7465"""
    expected = nx.Graph([(1, 2), (1, 5), (2, 3), (2, 4), (3, 5)])
    nx.utils.graphs_equal(nx.parse_adjlist(lines, delimiter=delim), expected)

