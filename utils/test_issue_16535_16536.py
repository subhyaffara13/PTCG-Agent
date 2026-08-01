
def test_issue_16535_16536():
    from sympy.functions.special.gamma_functions import (lowergamma, uppergamma)

    a = symbols('a')
    expr1 = lowergamma(a, x)
    expr2 = uppergamma(a, x)

    prntr = SciPyPrinter()
    assert prntr.doprint(expr1) == 'scipy.special.gamma(a)*scipy.special.gammainc(a, x)'
    assert prntr.doprint(expr2) == 'scipy.special.gamma(a)*scipy.special.gammaincc(a, x)'

    p_numpy = NumPyPrinter()
    p_pycode = PythonCodePrinter({'strict': False})

    for expr in [expr1, expr2]:
        with raises(NotImplementedError):
            p_numpy.doprint(expr1)
        assert "Not supported" in p_pycode.doprint(expr)

