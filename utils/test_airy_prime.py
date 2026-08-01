
def test_airy_prime():
    from sympy.functions.special.bessel import (airyaiprime, airybiprime)

    expr1 = airyaiprime(x)
    expr2 = airybiprime(x)

    prntr = SciPyPrinter()
    assert prntr.doprint(expr1) == 'scipy.special.airy(x)[1]'
    assert prntr.doprint(expr2) == 'scipy.special.airy(x)[3]'

    prntr = NumPyPrinter({'strict': False})
    assert "Not supported" in prntr.doprint(expr1)
    assert "Not supported" in prntr.doprint(expr2)

    prntr = PythonCodePrinter({'strict': False})
    assert "Not supported" in prntr.doprint(expr1)
    assert "Not supported" in prntr.doprint(expr2)

