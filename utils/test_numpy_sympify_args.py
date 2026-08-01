
def test_numpy_sympify_args():
    # Issue 15098. Make sure sympify args work with numpy types (like numpy.str_)
    if not numpy:
        skip("numpy not installed.")

    a = sympify(numpy.str_('a'))
    assert type(a) is Symbol
    assert a == Symbol('a')

    class CustomSymbol(Symbol):
        pass

    a = sympify(numpy.str_('a'), {"Symbol": CustomSymbol})
    assert isinstance(a, CustomSymbol)

    a = sympify(numpy.str_('x^y'))
    assert a == x**y
    a = sympify(numpy.str_('x^y'), convert_xor=False)
    assert a == Xor(x, y)

    raises(SympifyError, lambda: sympify(numpy.str_('x'), strict=True))

    a = sympify(numpy.str_('1.1'))
    assert isinstance(a, Float)
    assert a == 1.1

    a = sympify(numpy.str_('1.1'), rational=True)
    assert isinstance(a, Rational)
    assert a == Rational(11, 10)

    a = sympify(numpy.str_('x + x'))
    assert isinstance(a, Mul)
    assert a == 2*x

    a = sympify(numpy.str_('x + x'), evaluate=False)
    assert isinstance(a, Add)
    assert a == Add(x, x, evaluate=False)

