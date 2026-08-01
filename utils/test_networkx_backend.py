
def test_networkx_backend():
    """Test using `backend="networkx"` in a dispatchable function."""
    # (Implementing this test is harder than it should be)
    from networkx.classes.tests.dispatch_interface import (
        LoopbackBackendInterface,
        LoopbackGraph,
    )

    G = LoopbackGraph()
    G.add_edges_from([(0, 1), (1, 2), (1, 3), (2, 4)])

    @staticmethod
    def convert_to_nx(obj, *, name=None):
        if isinstance(obj, LoopbackGraph):
            new_graph = nx.Graph()
            new_graph.__dict__.update(obj.__dict__)
            return new_graph
        return obj

    # *This mutates LoopbackBackendInterface!*
    # This uses the same trick as in the previous test.
    orig_convert_to_nx = LoopbackBackendInterface.convert_to_nx
    LoopbackBackendInterface.convert_to_nx = convert_to_nx
    try:
        G2 = nx.ego_graph(G, 0, backend="networkx")
        assert type(G2) is nx.Graph
    finally:
        LoopbackBackendInterface.convert_to_nx = staticmethod(orig_convert_to_nx)

