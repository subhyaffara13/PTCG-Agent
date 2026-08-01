
def test_FunctionDefinition_print():
    x = symbols('x')
    n = symbols('n', integer=True)
    vx = Variable(x, type=real)
    vn = Variable(n, type=integer)
    body = [Assignment(x, x**n), Return(x)]
    fd1 = FunctionDefinition(real, 'power', [vx, vn], body)
    # Should be changed to proper test once multi-line generation is working
    # see https://github.com/sympy/sympy/issues/15824
    raises(NotImplementedError, lambda: fcode(fd1))

