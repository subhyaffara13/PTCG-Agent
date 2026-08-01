
def test_as_leading_term():
    assert (3 + 2*x**(log(3)/log(2) - 1)).as_leading_term(x) == 3
    assert (1/x**2 + 1 + x + x**2).as_leading_term(x) == 1/x**2
    assert (1/x + 1 + x + x**2).as_leading_term(x) == 1/x
    assert (x**2 + 1/x).as_leading_term(x) == 1/x
    assert (1 + x**2).as_leading_term(x) == 1
    assert (x + 1).as_leading_term(x) == 1
    assert (x + x**2).as_leading_term(x) == x
    assert (x**2).as_leading_term(x) == x**2
    assert (x + oo).as_leading_term(x) is oo

    raises(ValueError, lambda: (x + 1).as_leading_term(1))

    # https://github.com/sympy/sympy/issues/21177
    e = -3*x + (x + Rational(3, 2) - sqrt(3)*S.ImaginaryUnit/2)**2\
        - Rational(3, 2) + 3*sqrt(3)*S.ImaginaryUnit/2
    assert e.as_leading_term(x) == -sqrt(3)*I*x

    # https://github.com/sympy/sympy/issues/21245
    e = 1 - x - x**2
    d = (1 + sqrt(5))/2
    assert e.subs(x, y + 1/d).as_leading_term(y) == \
        (-40*y - 16*sqrt(5)*y)/(16 + 8*sqrt(5))

    # https://github.com/sympy/sympy/issues/26991
    assert sinh(tanh(3/(100*x))).as_leading_term(x, cdir = 1) == sinh(1)

