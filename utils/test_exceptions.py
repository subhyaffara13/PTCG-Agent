
def test_exceptions():
    I = QQ.old_poly_ring(x).ideal(x)
    J = QQ.old_poly_ring(y).ideal(1)
    raises(ValueError, lambda: I.union(x))
    raises(ValueError, lambda: I + J)
    raises(ValueError, lambda: I * J)
    raises(ValueError, lambda: I.union(J))
    assert (I == J) is False
    assert I != J


def test_exceptions():
    X = MatrixSymbol('x', 10, 20)
    raises(IndexError, lambda: X[0:12, 2])
    raises(IndexError, lambda: X[0:9, 22])
    raises(IndexError, lambda: X[-1:5, 2])


def test_exceptions():
    S = Sum(x, (x, a, b))
    raises(ValueError, lambda: S.change_index(x, x**2, y))
    S = Sum(x, (x, a, b), (x, 1, 4))
    raises(ValueError, lambda: S.index(x))
    S = Sum(x, (x, a, b), (y, 1, 4))
    raises(ValueError, lambda: S.reorder([x]))
    S = Sum(x, (x, y, b), (y, 1, 4))
    raises(ReorderError, lambda: S.reorder_limit(0, 1))
    S = Sum(x*y, (x, a, b), (y, 1, 4))
    raises(NotImplementedError, lambda: S.is_convergent())


def test_exceptions():
    with pytest.raises(TypeError, match="is not a tree."):
        G = nx.complete_graph(3)
        tree_data(G, 0)
    with pytest.raises(TypeError, match="is not directed."):
        G = nx.path_graph(3)
        tree_data(G, 0)
    with pytest.raises(TypeError, match="is not weakly connected."):
        G = nx.path_graph(3, create_using=nx.DiGraph)
        G.add_edge(2, 0)
        G.add_node(3)
        tree_data(G, 0)
    with pytest.raises(nx.NetworkXError, match="must be different."):
        G = nx.MultiDiGraph()
        G.add_node(0)
        tree_data(G, 0, ident="node", children="node")


def test_exceptions():
    """Bad input should raise exception."""
    G = nx.florentine_families_graph()
    pytest.raises(nx.NetworkXUnfeasible, nx.maximal_independent_set, G, ["Smith"])
    pytest.raises(
        nx.NetworkXUnfeasible, nx.maximal_independent_set, G, ["Salviati", "Pazzi"]
    )
    # MaximalIndependentSet is not implemented for directed graphs
    pytest.raises(nx.NetworkXNotImplemented, nx.maximal_independent_set, nx.DiGraph(G))


def test_exceptions():
    G = nx.Graph()
    pytest.raises(nx.NetworkXError, nx.stoer_wagner, G)
    G.add_node(1)
    pytest.raises(nx.NetworkXError, nx.stoer_wagner, G)
    G.add_node(2)
    pytest.raises(nx.NetworkXError, nx.stoer_wagner, G)
    G.add_edge(1, 2, weight=-2)
    pytest.raises(nx.NetworkXError, nx.stoer_wagner, G)
    G = nx.DiGraph()
    pytest.raises(nx.NetworkXNotImplemented, nx.stoer_wagner, G)
    G = nx.MultiGraph()
    pytest.raises(nx.NetworkXNotImplemented, nx.stoer_wagner, G)
    G = nx.MultiDiGraph()
    pytest.raises(nx.NetworkXNotImplemented, nx.stoer_wagner, G)


def test_exceptions():
    test = Graph()
    test.add_node("a")
    pytest.raises(NetworkXError, asyn_fluidc, test, "hi")
    pytest.raises(NetworkXError, asyn_fluidc, test, -1)
    pytest.raises(NetworkXError, asyn_fluidc, test, 3)
    with pytest.raises(ValueError, match="must be greater than 0"):
        asyn_fluidc(test, 1, max_iter=0)
    test.add_node("b")
    pytest.raises(NetworkXError, asyn_fluidc, test, 1)


def test_exceptions():
    # TODO should this test more options?
    with pytest.raises(ValueError):
        plt.subplots(2, 2, sharex='blah')
    with pytest.raises(ValueError):
        plt.subplots(2, 2, sharey='blah')

