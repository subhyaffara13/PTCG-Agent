
def test_cross_module_gil_nested_custom_acquired():
    """Makes sure that the GIL can be nested acquired/acquired by another module
    from a GIL-acquired state using custom locking logic."""
    m.test_cross_module_gil_nested_custom_acquired()

