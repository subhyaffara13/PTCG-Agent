
def test_not_implemented():
    eq = x**2 + y**4 - 1**2 - 3**4
    assert diophantine(eq, syms=[x, y]) == {(9, 1), (1, 3)}


def test_not_implemented():
    f = Dispatcher('f')

    @f.register(object)
    def _(x):
        return 'default'

    @f.register(int)
    def _(x):
        if x % 2 == 0:
            return 'even'
        else:
            raise MDNotImplementedError()

    assert f('hello') == 'default'  # default behavior
    assert f(2) == 'even'          # specialized behavior
    assert f(3) == 'default'       # fall bac to default behavior
    assert raises(NotImplementedError, lambda: f(1, 2))


def test_not_implemented(G):
    """Check that non-randomness is not implemented for directed or multigraphs."""
    with pytest.raises(nx.NetworkXNotImplemented, match=r"not implemented for"):
        nx.non_randomness(G)


def test_not_implemented():
    G = nx.MultiGraph()
    pytest.raises(nx.NetworkXNotImplemented, EdgeComponentAuxGraph.construct, G)
    pytest.raises(nx.NetworkXNotImplemented, nx.k_edge_components, G, k=2)
    pytest.raises(nx.NetworkXNotImplemented, nx.k_edge_subgraphs, G, k=2)
    with pytest.raises(nx.NetworkXNotImplemented):
        next(bridge_components(G))
    with pytest.raises(nx.NetworkXNotImplemented):
        next(bridge_components(nx.DiGraph()))

