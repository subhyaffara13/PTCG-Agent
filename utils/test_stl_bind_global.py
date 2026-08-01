
def test_stl_bind_global():
    import pybind11_cross_module_tests as cm

    with pytest.raises(RuntimeError) as excinfo:
        cm.register_nonlocal_map()
    assert (
        str(excinfo.value) == 'generic_type: type "NonLocalMap" is already registered!'
    )

    with pytest.raises(RuntimeError) as excinfo:
        cm.register_nonlocal_vec()
    assert (
        str(excinfo.value) == 'generic_type: type "NonLocalVec" is already registered!'
    )

    with pytest.raises(RuntimeError) as excinfo:
        cm.register_nonlocal_map2()
    assert (
        str(excinfo.value) == 'generic_type: type "NonLocalMap2" is already registered!'
    )

