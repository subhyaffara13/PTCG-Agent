
def test_custom_Derivative_methods():
    class MyPrinter(SciPyPrinter):
        def _print_Derivative_cosm1(self, args, seq_orders):
            arg, = args
            order, = seq_orders
            return 'my_custom_cosm1(%s, deriv_order=%d)' % (self._print(arg), order)

        def _print_Derivative_atan2(self, args, seq_orders):
            arg1, arg2 = args
            ord1, ord2 = seq_orders
            return 'my_custom_atan2(%s, %s, deriv1=%d, deriv2=%d)' % (
                self._print(arg1), self._print(arg2), ord1, ord2
            )

    p = MyPrinter()
    cosm1_1 = cosm1(x).diff(x, evaluate=False)
    assert p.doprint(cosm1_1) == 'my_custom_cosm1(x, deriv_order=1)'
    atan2_2_3 = atan2(x, y).diff(x, 2, y, 3, evaluate=False)
    assert p.doprint(atan2_2_3) == 'my_custom_atan2(x, y, deriv1=2, deriv2=3)'

    try:
        p.doprint(expm1(x).diff(x, evaluate=False))
    except PrintMethodNotImplementedError as e:
        assert '_print_Derivative_expm1' in repr(e)
    else:
        assert False  # should have thrown

    try:
        p.doprint(Derivative(cosm1(x**2),x))
    except ValueError as e:
        assert '_print_Derivative(' in repr(e)
    else:
        assert False  # should have thrown

