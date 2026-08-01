
def test_jax_custom_print_method():

    class expm1(Function):

        def _jaxcode(self, printer):
            x, = self.args
            function = f'expm1({printer._print(x)})'
            return printer._module_format(printer._module + '.' + function)

    printer = JaxPrinter()
    assert printer.doprint(expm1(Symbol('x'))) == 'jax.numpy.expm1(x)'

