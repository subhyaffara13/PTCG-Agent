
def test_is_empty():
    for s in [S.Naturals, S.Naturals0, S.Integers, S.Rationals, S.Reals,
            S.UniversalSet]:
        assert s.is_empty is False

    assert S.EmptySet.is_empty is True


def test_is_empty():
    graphs = [nx.Graph(), nx.DiGraph(), nx.MultiGraph(), nx.MultiDiGraph()]
    for G in graphs:
        assert nx.is_empty(G)
        G.add_nodes_from(range(5))
        assert nx.is_empty(G)
        G.add_edges_from([(1, 2), (3, 4)])
        assert not nx.is_empty(G)

