
def test_cross_module_gil_inner_pybind11_acquired():
    """Makes sure that the GIL can be acquired/acquired by another module
    from a GIL-acquired state using pybind11 locking logic."""
    m.test_cross_module_gil_inner_pybind11_acquired()

