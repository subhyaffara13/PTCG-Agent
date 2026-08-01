
def test_entry_point_name_is_module(clear_backend_registry):
    with pytest.raises(RuntimeError):
        backend_registry._validate_and_store_entry_points(
            [('module://backend.something', 'module1')])

