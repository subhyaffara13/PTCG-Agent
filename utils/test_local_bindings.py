
def test_local_bindings():
    """Tests that duplicate `py::module_local` class bindings work across modules"""

    # Make sure we can load the second module with the conflicting (but local) definition:
    import pybind11_cross_module_tests as cm

    i1 = m.LocalType(5)
    assert i1.get() == 4
    assert i1.get3() == 8

    i2 = cm.LocalType(10)
    assert i2.get() == 11
    assert i2.get2() == 12

    assert not hasattr(i1, "get2")
    assert not hasattr(i2, "get3")

    # Loading within the local module
    assert m.local_value(i1) == 5
    assert cm.local_value(i2) == 10

    # Cross-module loading works as well (on failure, the type loader looks for
    # external module-local converters):
    assert m.local_value(i2) == 10
    assert cm.local_value(i1) == 5

