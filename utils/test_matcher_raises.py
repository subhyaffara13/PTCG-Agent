
def test_matcher_raises(G1, G2):
    undirected_matchers = [iso.GraphMatcher, iso.MultiGraphMatcher]
    directed_matchers = [iso.DiGraphMatcher, iso.MultiDiGraphMatcher]

    for matcher in undirected_matchers:
        matcher(G1, G2)

        msg = r"\(Multi-\)GraphMatcher\(\) not defined for directed graphs"
        with pytest.raises(nx.NetworkXError, match=msg):
            matcher(G1.to_directed(), G2.to_directed())

    for matcher in directed_matchers:
        matcher(G1.to_directed(), G2.to_directed())

        msg = r"\(Multi-\)DiGraphMatcher\(\) not defined for undirected graphs"
        with pytest.raises(nx.NetworkXError, match=msg):
            matcher(G1, G2)

    for matcher in undirected_matchers + directed_matchers:
        msg = r"G1 and G2 must have the same directedness"
        with pytest.raises(nx.NetworkXError, match=msg):
            matcher(G1, G2.to_directed())
        with pytest.raises(nx.NetworkXError, match=msg):
            matcher(G1.to_directed(), G2)

