
def test_lambdify_Derivative_custom_printer():
    func1 = Function('func1')
    func2 = Function('func2')

    class MyPrinter(NumPyPrinter):

        def _print_Derivative_func1(self, args, seq_orders):
            arg, = args
            order, = seq_orders
            return '42'

    expr1 = func1(x).diff(x)
    raises(PrintMethodNotImplementedError, lambda: lambdify([x], expr1))
    f1 = lambdify([x], expr1, printer=MyPrinter)
    assert f1(7) == 42

    expr2 = func2(x).diff(x)
    raises(PrintMethodNotImplementedError, lambda: lambdify([x], expr2, printer=MyPrinter))

