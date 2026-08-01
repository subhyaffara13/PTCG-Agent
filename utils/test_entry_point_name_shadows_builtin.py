
def test_entry_point_name_shadows_builtin(clear_backend_registry):
    with pytest.raises(RuntimeError):
        backend_registry._validate_and_store_entry_points(
            [('qtagg', 'module1')])

