
def test_graph_converter_needs_backend():
    # When testing, `nx.from_scipy_sparse_array` will *always* call the backend
    # implementation if it's implemented. If `backend=` isn't given, then the result
    # will be converted back to NetworkX via `convert_to_nx`.
    # If not testing, then calling `nx.from_scipy_sparse_array` w/o `backend=` will
    # always call the original version. `backend=` is *required* to call the backend.
    from networkx.classes.tests.dispatch_interface import (
        LoopbackBackendInterface,
        LoopbackGraph,
    )

    A = sp.sparse.coo_array([[0, 3, 2], [3, 0, 1], [2, 1, 0]])

    side_effects = []

    def from_scipy_sparse_array(self, *args, **kwargs):
        side_effects.append(1)  # Just to prove this was called
        return self.convert_from_nx(
            self.__getattr__("from_scipy_sparse_array")(*args, **kwargs),
            preserve_edge_attrs=True,
            preserve_node_attrs=True,
            preserve_graph_attrs=True,
        )

    @staticmethod
    def convert_to_nx(obj, *, name=None):
        if type(obj) is nx.Graph:
            return obj
        return nx.Graph(obj)

    # *This mutates LoopbackBackendInterface!*
    orig_convert_to_nx = LoopbackBackendInterface.convert_to_nx
    LoopbackBackendInterface.convert_to_nx = convert_to_nx
    LoopbackBackendInterface.from_scipy_sparse_array = from_scipy_sparse_array

    try:
        assert side_effects == []
        assert type(nx.from_scipy_sparse_array(A)) is nx.Graph
        assert side_effects == [1]
        assert (
            type(nx.from_scipy_sparse_array(A, backend="nx_loopback")) is LoopbackGraph
        )
        assert side_effects == [1, 1]
        # backend="networkx" is default implementation
        assert type(nx.from_scipy_sparse_array(A, backend="networkx")) is nx.Graph
        assert side_effects == [1, 1]
    finally:
        LoopbackBackendInterface.convert_to_nx = staticmethod(orig_convert_to_nx)
        del LoopbackBackendInterface.from_scipy_sparse_array
    with pytest.raises(ImportError, match="backend is not installed"):
        nx.from_scipy_sparse_array(A, backend="bad-backend-name")

