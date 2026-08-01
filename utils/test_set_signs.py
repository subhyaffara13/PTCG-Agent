
def test_set_signs():
    assert limit(abs(x), x, 0) == 0
    assert limit(abs(sin(x)), x, 0) == 0
    assert limit(abs(cos(x)), x, 0) == 1
    assert limit(abs(sin(x + 1)), x, 0) == sin(1)

    # https://github.com/sympy/sympy/issues/9449
    assert limit((Abs(x + y) - Abs(x - y))/(2*x), x, 0) == sign(y)

    # https://github.com/sympy/sympy/issues/12398
    assert limit(Abs(log(x)/x**3), x, oo) == 0
    assert limit(x*(Abs(log(x)/x**3)/Abs(log(x + 1)/(x + 1)**3) - 1), x, oo) == 3

    # https://github.com/sympy/sympy/issues/18501
    assert limit(Abs(log(x - 1)**3 - 1), x, 1, '+') == oo

    # https://github.com/sympy/sympy/issues/18997
    assert limit(Abs(log(x)), x, 0) == oo
    assert limit(Abs(log(Abs(x))), x, 0) == oo

    # https://github.com/sympy/sympy/issues/19026
    z = Symbol('z', positive=True)
    assert limit(Abs(log(z) + 1)/log(z), z, oo) == 1

    # https://github.com/sympy/sympy/issues/20704
    assert limit(z*(Abs(1/z + y) - Abs(y - 1/z))/2, z, 0) == 0

    # https://github.com/sympy/sympy/issues/21606
    assert limit(cos(z)/sign(z), z, pi, '-') == -1

