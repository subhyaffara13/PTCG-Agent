
def test_asia_graph_dsep(asia_graph):
    """Example-based test of d-separation for asia_graph."""
    assert nx.is_d_separator(
        asia_graph, {"asia", "smoking"}, {"dyspnea", "xray"}, {"bronchitis", "either"}
    )
    assert nx.is_d_separator(
        asia_graph, {"tuberculosis", "cancer"}, {"bronchitis"}, {"smoking", "xray"}
    )

