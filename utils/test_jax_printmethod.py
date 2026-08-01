
def test_jax_printmethod():
    printer = JaxPrinter()
    assert hasattr(printer, 'printmethod')
    assert printer.printmethod == '_jaxcode'

