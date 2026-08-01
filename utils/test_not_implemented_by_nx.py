
def test_not_implemented_by_nx():
    assert "networkx" in nx.pagerank.backends
    assert "networkx" not in _stub_func.backends

    if "nx_loopback" in nx.config.backends:
        from networkx.classes.tests.dispatch_interface import LoopbackBackendInterface

        def stub_func_implementation(G):
            return True

        LoopbackBackendInterface._stub_func = staticmethod(stub_func_implementation)
        try:
            assert _stub_func(nx.Graph()) is True
        finally:
            del LoopbackBackendInterface._stub_func

    with pytest.raises(NotImplementedError):
        _stub_func(nx.Graph())

