
def test_cross_module_gil_released():
    """Makes sure that the GIL can be acquired by another module from a GIL-released state."""
    m.test_cross_module_gil_released()  # Should not raise a SIGSEGV

