
def test_FunctionPrototype_print():
    x = symbols('x')
    n = symbols('n', integer=True)
    vx = Variable(x, type=real)
    vn = Variable(n, type=integer)
    fp1 = FunctionPrototype(real, 'power', [vx, vn])
    # Should be changed to proper test once multi-line generation is working
    # see https://github.com/sympy/sympy/issues/15824
    raises(NotImplementedError, lambda: fcode(fp1))

