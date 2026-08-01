
def test_cross_module_gil_nested_pybind11_released():
    """Makes sure that the GIL can be nested acquired/released by another module
    from a GIL-released state using pybind11 locking logic."""
    m.test_cross_module_gil_nested_pybind11_released()

