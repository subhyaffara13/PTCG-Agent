
def test_cross_module_gil_acquired():
    """Makes sure that the GIL can be acquired by another module from a GIL-acquired state."""
    m.test_cross_module_gil_acquired()  # Should not raise a SIGSEGV

