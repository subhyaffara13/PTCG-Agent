
def test_cupy_print_methods():
    prntr = CuPyPrinter()
    assert hasattr(prntr, '_print_acos')
    assert hasattr(prntr, '_print_log')

