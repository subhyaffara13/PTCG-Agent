
def test_cross_module_gil_inner_custom_released():
    """Makes sure that the GIL can be acquired/released by another module
    from a GIL-released state using custom locking logic."""
    m.test_cross_module_gil_inner_custom_released()

