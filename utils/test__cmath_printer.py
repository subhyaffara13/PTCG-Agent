
def test_CmathPrinter():
    p = CmathPrinter()

    assert p.doprint(sqrt(x)) == 'cmath.sqrt(x)'
    assert p.doprint(log(x)) == 'cmath.log(x)'

    assert p.doprint(sin(x)) == 'cmath.sin(x)'
    assert p.doprint(cos(x)) == 'cmath.cos(x)'
    assert p.doprint(tan(x)) == 'cmath.tan(x)'

    assert p.doprint(asin(x)) == 'cmath.asin(x)'
    assert p.doprint(acos(x)) == 'cmath.acos(x)'
    assert p.doprint(atan(x)) == 'cmath.atan(x)'

    assert p.doprint(sinh(x)) == 'cmath.sinh(x)'
    assert p.doprint(cosh(x)) == 'cmath.cosh(x)'
    assert p.doprint(tanh(x)) == 'cmath.tanh(x)'

    assert p.doprint(asinh(x)) == 'cmath.asinh(x)'
    assert p.doprint(acosh(x)) == 'cmath.acosh(x)'
    assert p.doprint(atanh(x)) == 'cmath.atanh(x)'

