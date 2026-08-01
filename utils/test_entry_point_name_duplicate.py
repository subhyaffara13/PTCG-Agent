
def test_entry_point_name_duplicate(clear_backend_registry):
    with pytest.raises(RuntimeError):
        backend_registry._validate_and_store_entry_points(
            [('some_name', 'module1'), ('some_name', 'module2')])

