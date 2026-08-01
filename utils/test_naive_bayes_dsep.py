
def test_naive_bayes_dsep(naive_bayes_graph):
    """Example-based test of d-separation for naive_bayes_graph."""
    for u, v in combinations(range(1, 5), 2):
        assert nx.is_d_separator(naive_bayes_graph, {u}, {v}, {0})
        assert not nx.is_d_separator(naive_bayes_graph, {u}, {v}, set())

