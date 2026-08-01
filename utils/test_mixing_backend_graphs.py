
def test_mixing_backend_graphs():
    from networkx.classes.tests import dispatch_interface

    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    H = nx.Graph()
    H.add_edge(2, 3)
    rv = nx.intersection(G, H)
    assert set(nx.intersection(G, H)) == {2, 3}
    G2 = dispatch_interface.convert(G)
    H2 = dispatch_interface.convert(H)
    if "nx_loopback" in nx.config.backend_priority:
        # Auto-convert
        assert set(nx.intersection(G2, H)) == {2, 3}
        assert set(nx.intersection(G, H2)) == {2, 3}
    elif not nx.config.backend_priority and "nx_loopback" not in nx.config.backends:
        # G2 and H2 are backend objects for a backend that is not registered!
        with pytest.raises(ImportError, match="backend is not installed"):
            nx.intersection(G2, H)
        with pytest.raises(ImportError, match="backend is not installed"):
            nx.intersection(G, H2)

