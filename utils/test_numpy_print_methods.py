
def test_numpy_print_methods():
    prntr = NumPyPrinter()
    assert hasattr(prntr, '_print_acos')
    assert hasattr(prntr, '_print_log')

