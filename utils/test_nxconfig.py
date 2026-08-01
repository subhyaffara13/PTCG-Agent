
def test_nxconfig():
    assert isinstance(nx.config.backend_priority, BackendPriorities)
    assert isinstance(nx.config.backend_priority.algos, list)
    assert isinstance(nx.config.backends, Config)
    with pytest.raises(TypeError, match="must be a list of backend names"):
        nx.config.backend_priority.algos = "nx_loopback"
    with pytest.raises(ValueError, match="Unknown backend when setting"):
        nx.config.backend_priority.algos = ["this_almost_certainly_is_not_a_backend"]
    with pytest.raises(TypeError, match="must be a Config of backend configs"):
        nx.config.backends = {}
    with pytest.raises(TypeError, match="must be a Config of backend configs"):
        nx.config.backends = Config(plausible_backend_name={})
    with pytest.raises(ValueError, match="Unknown backend when setting"):
        nx.config.backends = Config(this_almost_certainly_is_not_a_backend=Config())
    with pytest.raises(TypeError, match="must be True or False"):
        nx.config.cache_converted_graphs = "bad value"
    with pytest.raises(TypeError, match="must be a set of "):
        nx.config.warnings_to_ignore = 7
    with pytest.raises(ValueError, match="Unknown warning "):
        nx.config.warnings_to_ignore = {"bad value"}

    prev = nx.config.backend_priority
    try:
        nx.config.backend_priority = ["networkx"]
        assert isinstance(nx.config.backend_priority, BackendPriorities)
        assert nx.config.backend_priority.algos == ["networkx"]
    finally:
        nx.config.backend_priority = prev

