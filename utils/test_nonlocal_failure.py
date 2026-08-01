
def test_nonlocal_failure():
    """Tests that attempting to register a non-local type in multiple modules fails"""
    import pybind11_cross_module_tests as cm

    with pytest.raises(RuntimeError) as excinfo:
        cm.register_nonlocal()
    assert (
        str(excinfo.value) == 'generic_type: type "NonLocalType" is already registered!'
    )

