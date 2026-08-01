
def test_fresnel_integrals():
    from sympy.functions.special.error_functions import (fresnelc, fresnels)

    expr1 = fresnelc(x)
    expr2 = fresnels(x)

    prntr = SciPyPrinter()
    assert prntr.doprint(expr1) == 'scipy.special.fresnel(x)[1]'
    assert prntr.doprint(expr2) == 'scipy.special.fresnel(x)[0]'

    p_numpy = NumPyPrinter()
    p_pycode = PythonCodePrinter()
    p_mpmath = MpmathPrinter()
    for expr in [expr1, expr2]:
        with raises(NotImplementedError):
            p_numpy.doprint(expr)
        with raises(NotImplementedError):
            p_pycode.doprint(expr)

    assert p_mpmath.doprint(expr1) == 'mpmath.fresnelc(x)'
    assert p_mpmath.doprint(expr2) == 'mpmath.fresnels(x)'

