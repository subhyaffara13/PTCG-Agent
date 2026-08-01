
def test_jax_print_methods():
    prntr = JaxPrinter()
    assert hasattr(prntr, '_print_acos')
    assert hasattr(prntr, '_print_log')

