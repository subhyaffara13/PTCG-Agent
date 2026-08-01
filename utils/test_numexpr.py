
def test_numexpr():
    # test ITE rewrite as Piecewise
    from sympy.logic.boolalg import ITE
    expr = ITE(x > 0, True, False, evaluate=False)
    assert NumExprPrinter().doprint(expr) == \
           "numexpr.evaluate('where((x > 0), True, False)', truediv=True)"

    from sympy.codegen.ast import Return, FunctionDefinition, Variable, Assignment
    func_def = FunctionDefinition(None, 'foo', [Variable(x)], [Assignment(y,x), Return(y**2)])
    expected = "def foo(x):\n"\
               "    y = numexpr.evaluate('x', truediv=True)\n"\
               "    return numexpr.evaluate('y**2', truediv=True)"
    assert NumExprPrinter().doprint(func_def) == expected

