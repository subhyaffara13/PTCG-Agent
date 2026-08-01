
def test_entry_point_identical(clear_backend_registry):
    # Issue https://github.com/matplotlib/matplotlib/issues/28367
    # Multiple entry points with the same name and value (value is the module)
    # are acceptable.
    n = len(backend_registry._name_to_module)
    backend_registry._validate_and_store_entry_points(
        [('some_name', 'some.module'), ('some_name', 'some.module')])
    assert len(backend_registry._name_to_module) == n+1
    assert backend_registry._name_to_module['some_name'] == 'module://some.module'

