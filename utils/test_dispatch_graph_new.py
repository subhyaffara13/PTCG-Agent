
def test_dispatch_graph_new():
    from networkx.classes.tests.dispatch_interface import LoopbackGraph

    G = nx.Graph()
    assert not isinstance(G, LoopbackGraph)

    # `backend=` argument that gets passed to __init__ is ignored.
    # Best practice is that it should not be in the `.graph` dict.
    G = nx.Graph(backend="networkx")
    assert type(G) is nx.Graph
    assert "backend" not in G.graph

    G = nx.Graph(backend="nx_loopback")
    assert isinstance(G, LoopbackGraph)
    assert "backend" not in G.graph

    # Args are passed
    G1 = nx.Graph([(0, 1), (1, 2)])
    assert not isinstance(G1, LoopbackGraph)
    G2 = nx.Graph([(0, 1), (1, 2)], backend="nx_loopback")
    assert isinstance(G2, LoopbackGraph)
    assert nx.utils.misc.graphs_equal(G1, G2)

    # Test config for automatic usage
    with nx.config.backend_priority(classes=["nx_loopback"]):
        G = nx.Graph()
        assert isinstance(G, LoopbackGraph)
        # LoopbackDiGraph __new__ is not implemented
        G = nx.DiGraph()
        assert not isinstance(G, LoopbackGraph)
    G = nx.Graph()
    assert not isinstance(G, LoopbackGraph)

