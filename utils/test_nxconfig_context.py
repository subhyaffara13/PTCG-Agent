
def test_nxconfig_context():
    # We do some special handling so that `nx.config.backend_priority = val`
    # actually does `nx.config.backend_priority.algos = val`.
    orig = nx.config.backend_priority.algos
    val = [] if orig else ["networkx"]
    assert orig != val
    assert nx.config.backend_priority.algos != val
    with nx.config(backend_priority=val):
        assert nx.config.backend_priority.algos == val
    assert nx.config.backend_priority.algos == orig
    with nx.config.backend_priority(algos=val):
        assert nx.config.backend_priority.algos == val
    assert nx.config.backend_priority.algos == orig
    bad = ["bad-backend"]
    with pytest.raises(ValueError, match="Unknown backend"):
        nx.config.backend_priority = bad
    with pytest.raises(ValueError, match="Unknown backend"):
        with nx.config(backend_priority=bad):
            pass
    with pytest.raises(ValueError, match="Unknown backend"):
        with nx.config.backend_priority(algos=bad):
            pass

