
def test_load_entry_points_only_if_needed(clear_backend_registry, backend):
    assert not backend_registry._loaded_entry_points
    check = backend_registry.resolve_backend(backend)
    assert check == (backend, None)
    assert not backend_registry._loaded_entry_points
    backend_registry.list_all()  # Force load of entry points
    assert backend_registry._loaded_entry_points

