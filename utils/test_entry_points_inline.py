
def test_entry_points_inline():
    pytest.importorskip('matplotlib_inline')
    backends = backend_registry.list_all()
    assert 'inline' in backends

