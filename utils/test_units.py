
def test_units():
    assert solve(1/x - 1/(2*cm)) == [2*cm]


def test_units():
    assert solveset_real(1/x - 1/(2*cm), x) == FiniteSet(2*cm)


def test_units():
    expr = joule
    ascii_str1 = \
"""\
              2\n\
kilogram*meter \n\
---------------\n\
          2    \n\
    second     \
"""
    unicode_str1 = \
"""\
              2\n\
kilogram⋅meter \n\
───────────────\n\
          2    \n\
    second     \
"""

    ascii_str2 = \
"""\
                    2\n\
3*x*y*kilogram*meter \n\
---------------------\n\
             2       \n\
       second        \
"""
    unicode_str2 = \
"""\
                    2\n\
3⋅x⋅y⋅kilogram⋅meter \n\
─────────────────────\n\
             2       \n\
       second        \
"""

    from sympy.physics.units import kg, m, s
    assert upretty(expr) == "joule"
    assert pretty(expr) == "joule"
    assert upretty(expr.convert_to(kg*m**2/s**2)) == unicode_str1
    assert pretty(expr.convert_to(kg*m**2/s**2)) == ascii_str1
    assert upretty(3*kg*x*m**2*y/s**2) == unicode_str2
    assert pretty(3*kg*x*m**2*y/s**2) == ascii_str2


def test_units():
    R = QQ.old_poly_ring(x)
    assert R.is_unit(R.convert(1))
    assert R.is_unit(R.convert(2))
    assert not R.is_unit(R.convert(x))
    assert not R.is_unit(R.convert(1 + x))

    R = QQ.old_poly_ring(x, order='ilex')
    assert R.is_unit(R.convert(1))
    assert R.is_unit(R.convert(2))
    assert not R.is_unit(R.convert(x))
    assert R.is_unit(R.convert(1 + x))

    R = ZZ.old_poly_ring(x)
    assert R.is_unit(R.convert(1))
    assert not R.is_unit(R.convert(2))
    assert not R.is_unit(R.convert(x))
    assert not R.is_unit(R.convert(1 + x))


def test_units():
    assert convert_to((5*m/s * day) / km, 1) == 432
    assert convert_to(foot / meter, meter) == Rational(3048, 10000)
    # amu is a pure mass so mass/mass gives a number, not an amount (mol)
    # TODO: need better simplification routine:
    assert str(convert_to(grams/amu, grams).n(2)) == '6.0e+23'

    # Light from the sun needs about 8.3 minutes to reach earth
    t = (1*au / speed_of_light) / minute
    # TODO: need a better way to simplify expressions containing units:
    t = convert_to(convert_to(t, meter / minute), meter)
    assert t.simplify() == Rational(49865956897, 5995849160)

    # TODO: fix this, it should give `m` without `Abs`
    assert sqrt(m**2) == m
    assert (sqrt(m))**2 == m

    t = Symbol('t')
    assert integrate(t*m/s, (t, 1*s, 5*s)) == 12*m*s
    assert (t * m/s).integrate((t, 1*s, 5*s)) == 12*m*s

