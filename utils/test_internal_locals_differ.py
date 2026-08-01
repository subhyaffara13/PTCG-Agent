
def test_internal_locals_differ():
    """Makes sure the internal local type map differs across the two modules"""
    import pybind11_cross_module_tests as cm

    assert m.local_cpp_types_addr() != cm.local_cpp_types_addr()

