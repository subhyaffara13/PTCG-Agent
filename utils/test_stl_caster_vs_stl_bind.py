
def test_stl_caster_vs_stl_bind(msg):
    """One module uses a generic vector caster from `<pybind11/stl.h>` while the other
    exports `std::vector<int>` via `py:bind_vector` and `py::module_local`"""
    import pybind11_cross_module_tests as cm

    v1 = cm.VectorInt([1, 2, 3])
    assert m.load_vector_via_caster(v1) == 6
    assert cm.load_vector_via_binding(v1) == 6

    v2 = [1, 2, 3]
    assert m.load_vector_via_caster(v2) == 6
    with pytest.raises(TypeError) as excinfo:
        cm.load_vector_via_binding(v2)
    assert (
        msg(excinfo.value)
        == """
    load_vector_via_binding(): incompatible function arguments. The following argument types are supported:
        1. (arg0: pybind11_cross_module_tests.VectorInt) -> int

    Invoked with: [1, 2, 3]
    """
    )

