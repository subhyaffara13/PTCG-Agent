from typing import Tuple

def test_piecewise1():

    # Test canonicalization
    assert Piecewise((x, x < 1.)).has(1.0)  # doesn't get changed to x < 1
    assert unchanged(Piecewise, ExprCondPair(x, x < 1), ExprCondPair(0, True))
    assert Piecewise((x, x < 1), (0, True)) == Piecewise(ExprCondPair(x, x < 1),
                                                         ExprCondPair(0, True))
    assert Piecewise((x, x < 1), (0, True), (1, True)) == \
        Piecewise((x, x < 1), (0, True))
    assert Piecewise((x, x < 1), (0, False), (-1, 1 > 2)) == \
        Piecewise((x, x < 1))
    assert Piecewise((x, x < 1), (0, x < 1), (0, True)) == \
        Piecewise((x, x < 1), (0, True))
    assert Piecewise((x, x < 1), (0, x < 2), (0, True)) == \
        Piecewise((x, x < 1), (0, True))
    assert Piecewise((x, x < 1), (x, x < 2), (0, True)) == \
        Piecewise((x, Or(x < 1, x < 2)), (0, True))
    assert Piecewise((x, x < 1), (x, x < 2), (x, True)) == x
    assert Piecewise((x, True)) == x
    # Explicitly constructed empty Piecewise not accepted
    raises(TypeError, lambda: Piecewise())
    # False condition is never retained
    assert Piecewise((2*x, x < 0), (x, False)) == \
        Piecewise((2*x, x < 0), (x, False), evaluate=False) == \
        Piecewise((2*x, x < 0))
    assert Piecewise((x, False)) == Undefined
    raises(TypeError, lambda: Piecewise(x))
    assert Piecewise((x, 1)) == x  # 1 and 0 are accepted as True/False
    raises(TypeError, lambda: Piecewise((x, 2)))
    raises(TypeError, lambda: Piecewise((x, x**2)))
    raises(TypeError, lambda: Piecewise(([1], True)))
    assert Piecewise(((1, 2), True)) == Tuple(1, 2)
    cond = (Piecewise((1, x < 0), (2, True)) < y)
    assert Piecewise((1, cond)
        ) == Piecewise((1, ITE(x < 0, y > 1, y > 2)))

    assert Piecewise((1, x > 0), (2, And(x <= 0, x > -1))
        ) == Piecewise((1, x > 0), (2, x > -1))
    assert Piecewise((1, x <= 0), (2, (x < 0) & (x > -1))
        ) == Piecewise((1, x <= 0))

    # test for supporting Contains in Piecewise
    pwise = Piecewise(
        (1, And(x <= 6, x > 1, Contains(x, S.Integers))),
        (0, True))
    assert pwise.subs(x, pi) == 0
    assert pwise.subs(x, 2) == 1
    assert pwise.subs(x, 7) == 0

    # Test subs
    p = Piecewise((-1, x < -1), (x**2, x < 0), (log(x), x >= 0))
    p_x2 = Piecewise((-1, x**2 < -1), (x**4, x**2 < 0), (log(x**2), x**2 >= 0))
    assert p.subs(x, x**2) == p_x2
    assert p.subs(x, -5) == -1
    assert p.subs(x, -1) == 1
    assert p.subs(x, 1) == log(1)

    # More subs tests
    p2 = Piecewise((1, x < pi), (-1, x < 2*pi), (0, x > 2*pi))
    p3 = Piecewise((1, Eq(x, 0)), (1/x, True))
    p4 = Piecewise((1, Eq(x, 0)), (2, 1/x>2))
    assert p2.subs(x, 2) == 1
    assert p2.subs(x, 4) == -1
    assert p2.subs(x, 10) == 0
    assert p3.subs(x, 0.0) == 1
    assert p4.subs(x, 0.0) == 1


    f, g, h = symbols('f,g,h', cls=Function)
    pf = Piecewise((f(x), x < -1), (f(x) + h(x) + 2, x <= 1))
    pg = Piecewise((g(x), x < -1), (g(x) + h(x) + 2, x <= 1))
    assert pg.subs(g, f) == pf

    assert Piecewise((1, Eq(x, 0)), (0, True)).subs(x, 0) == 1
    assert Piecewise((1, Eq(x, 0)), (0, True)).subs(x, 1) == 0
    assert Piecewise((1, Eq(x, y)), (0, True)).subs(x, y) == 1
    assert Piecewise((1, Eq(x, z)), (0, True)).subs(x, z) == 1
    assert Piecewise((1, Eq(exp(x), cos(z))), (0, True)).subs(x, z) == \
        Piecewise((1, Eq(exp(z), cos(z))), (0, True))

    p5 = Piecewise( (0, Eq(cos(x) + y, 0)), (1, True))
    assert p5.subs(y, 0) == Piecewise( (0, Eq(cos(x), 0)), (1, True))

    assert Piecewise((-1, y < 1), (0, x < 0), (1, Eq(x, 0)), (2, True)
        ).subs(x, 1) == Piecewise((-1, y < 1), (2, True))
    assert Piecewise((1, Eq(x**2, -1)), (2, x < 0)).subs(x, I) == 1

    p6 = Piecewise((x, x > 0))
    n = symbols('n', negative=True)
    assert p6.subs(x, n) == Undefined

    # Test evalf
    assert p.evalf() == Piecewise((-1.0, x < -1), (x**2, x < 0), (log(x), True))
    assert p.evalf(subs={x: -2}) == -1.0
    assert p.evalf(subs={x: -1}) == 1.0
    assert p.evalf(subs={x: 1}) == log(1)
    assert p6.evalf(subs={x: -5}) == Undefined

    # Test doit
    f_int = Piecewise((Integral(x, (x, 0, 1)), x < 1))
    assert f_int.doit() == Piecewise( (S.Half, x < 1) )

    # Test differentiation
    f = x
    fp = x*p
    dp = Piecewise((0, x < -1), (2*x, x < 0), (1/x, x >= 0))
    fp_dx = x*dp + p
    assert diff(p, x) == dp
    assert diff(f*p, x) == fp_dx

    # Test simple arithmetic
    assert x*p == fp
    assert x*p + p == p + x*p
    assert p + f == f + p
    assert p + dp == dp + p
    assert p - dp == -(dp - p)

    # Test power
    dp2 = Piecewise((0, x < -1), (4*x**2, x < 0), (1/x**2, x >= 0))
    assert dp**2 == dp2

    # Test _eval_interval
    f1 = x*y + 2
    f2 = x*y**2 + 3
    peval = Piecewise((f1, x < 0), (f2, x > 0))
    peval_interval = f1.subs(
        x, 0) - f1.subs(x, -1) + f2.subs(x, 1) - f2.subs(x, 0)
    assert peval._eval_interval(x, 0, 0) == 0
    assert peval._eval_interval(x, -1, 1) == peval_interval
    peval2 = Piecewise((f1, x < 0), (f2, True))
    assert peval2._eval_interval(x, 0, 0) == 0
    assert peval2._eval_interval(x, 1, -1) == -peval_interval
    assert peval2._eval_interval(x, -1, -2) == f1.subs(x, -2) - f1.subs(x, -1)
    assert peval2._eval_interval(x, -1, 1) == peval_interval
    assert peval2._eval_interval(x, None, 0) == peval2.subs(x, 0)
    assert peval2._eval_interval(x, -1, None) == -peval2.subs(x, -1)

    # Test integration
    assert p.integrate() == Piecewise(
        (-x, x < -1),
        (x**3/3 + Rational(4, 3), x < 0),
        (x*log(x) - x + Rational(4, 3), True))
    p = Piecewise((x, x < 1), (x**2, -1 <= x), (x, 3 < x))
    assert integrate(p, (x, -2, 2)) == Rational(5, 6)
    assert integrate(p, (x, 2, -2)) == Rational(-5, 6)
    p = Piecewise((0, x < 0), (1, x < 1), (0, x < 2), (1, x < 3), (0, True))
    assert integrate(p, (x, -oo, oo)) == 2
    p = Piecewise((x, x < -10), (x**2, x <= -1), (x, 1 < x))
    assert integrate(p, (x, -2, 2)) == Undefined

    # Test commutativity
    assert isinstance(p, Piecewise) and p.is_commutative is True

