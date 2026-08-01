
def test_Integral():
    assert mcode(Integral(sin(sin(x)), x)) == "Hold[Integrate[Sin[Sin[x]], x]]"
    assert mcode(Integral(exp(-x**2 - y**2),
                          (x, -oo, oo),
                          (y, -oo, oo))) == \
        "Hold[Integrate[Exp[-x^2 - y^2], {x, -Infinity, Infinity}, " \
        "{y, -Infinity, Infinity}]]"


def test_Integral():
    assert precedence(Integral(x, y)) == PRECEDENCE["Atom"]


def test_Integral():
    from sympy.functions.elementary.exponential import exp
    from sympy.integrals.integrals import Integral

    single = Integral(exp(-x), (x, 0, oo))
    double = Integral(x**2*exp(x*y), (x, -z, z), (y, 0, z))
    indefinite = Integral(x**2, x)
    evaluateat = Integral(x**2, (x, 1))

    prntr = SciPyPrinter()
    assert prntr.doprint(single) == 'scipy.integrate.quad(lambda x: numpy.exp(-x), 0, numpy.inf)[0]'
    assert prntr.doprint(double) == 'scipy.integrate.nquad(lambda x, y: x**2*numpy.exp(x*y), ((-z, z), (0, z)))[0]'
    raises(NotImplementedError, lambda: prntr.doprint(indefinite))
    raises(NotImplementedError, lambda: prntr.doprint(evaluateat))

    prntr = MpmathPrinter()
    assert prntr.doprint(single) == 'mpmath.quad(lambda x: mpmath.exp(-x), (0, mpmath.inf))'
    assert prntr.doprint(double) == 'mpmath.quad(lambda x, y: x**2*mpmath.exp(x*y), (-z, z), (0, z))'
    raises(NotImplementedError, lambda: prntr.doprint(indefinite))
    raises(NotImplementedError, lambda: prntr.doprint(evaluateat))


def test_Integral():
    assert str(Integral(sin(x), y)) == "Integral(sin(x), y)"
    assert str(Integral(sin(x), (y, 0, 1))) == "Integral(sin(x), (y, 0, 1))"

