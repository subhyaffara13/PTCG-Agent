
def test_entry_points_ipympl():
    pytest.importorskip('ipympl')
    backends = backend_registry.list_all()
    assert 'ipympl' in backends
    assert 'widget' in backends

