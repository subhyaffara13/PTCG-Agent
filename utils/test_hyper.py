
def test_hyper():
    expr = hyper((), (), z)
    ucode_str = \
"""\
 ┌─  ⎛  │  ⎞\n\
 ├─  ⎜  │ z⎟\n\
0╵ 0 ⎝  │  ⎠\
"""
    ascii_str = \
"""\
  _         \n\
 |_  /  |  \\\n\
 |   |  | z|\n\
0  0 \\  |  /\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = hyper((), (1,), x)
    ucode_str = \
"""\
 ┌─  ⎛  │  ⎞\n\
 ├─  ⎜  │ x⎟\n\
0╵ 1 ⎝1 │  ⎠\
"""
    ascii_str = \
"""\
  _         \n\
 |_  /  |  \\\n\
 |   |  | x|\n\
0  1 \\1 |  /\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = hyper([2], [1], x)
    ucode_str = \
"""\
 ┌─  ⎛2 │  ⎞\n\
 ├─  ⎜  │ x⎟\n\
1╵ 1 ⎝1 │  ⎠\
"""
    ascii_str = \
"""\
  _         \n\
 |_  /2 |  \\\n\
 |   |  | x|\n\
1  1 \\1 |  /\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = hyper((pi/3, -2*k), (3, 4, 5, -3), x)
    ucode_str = \
"""\
     ⎛  π         │  ⎞\n\
 ┌─  ⎜  ─, -2⋅k   │  ⎟\n\
 ├─  ⎜  3         │ x⎟\n\
2╵ 4 ⎜            │  ⎟\n\
     ⎝-3, 3, 4, 5 │  ⎠\
"""
    ascii_str = \
"""\
                      \n\
  _  / pi         |  \\\n\
 |_  | --, -2*k   |  |\n\
 |   | 3          | x|\n\
2  4 |            |  |\n\
     \\-3, 3, 4, 5 |  /\
"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = hyper((pi, S('2/3'), -2*k), (3, 4, 5, -3), x**2)
    ucode_str = \
"""\
 ┌─  ⎛2/3, π, -2⋅k │  2⎞\n\
 ├─  ⎜             │ x ⎟\n\
3╵ 4 ⎝-3, 3, 4, 5  │   ⎠\
"""
    ascii_str = \
"""\
  _                      \n\
 |_  /2/3, pi, -2*k |  2\\
 |   |              | x |
3  4 \\ -3, 3, 4, 5  |   /"""

    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = hyper([1, 2], [3, 4], 1/(1/(1/(1/x + 1) + 1) + 1))
    ucode_str = \
"""\
     ⎛     │       1      ⎞\n\
     ⎜     │ ─────────────⎟\n\
     ⎜     │         1    ⎟\n\
 ┌─  ⎜1, 2 │ 1 + ─────────⎟\n\
 ├─  ⎜     │           1  ⎟\n\
2╵ 2 ⎜3, 4 │     1 + ─────⎟\n\
     ⎜     │             1⎟\n\
     ⎜     │         1 + ─⎟\n\
     ⎝     │             x⎠\
"""

    ascii_str = \
"""\
                           \n\
     /     |       1      \\\n\
     |     | -------------|\n\
  _  |     |         1    |\n\
 |_  |1, 2 | 1 + ---------|\n\
 |   |     |           1  |\n\
2  2 |3, 4 |     1 + -----|\n\
     |     |             1|\n\
     |     |         1 + -|\n\
     \\     |             x/\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str


def test_hyper():
    raises(TypeError, lambda: hyper(1, 2, z))

    assert hyper((2, 1), (1,), z) == hyper(Tuple(1, 2), Tuple(1), z)
    assert hyper((2, 1, 2), (1, 2, 1, 3), z) == hyper((2,), (1, 3), z)
    u = hyper((2, 1, 2), (1, 2, 1, 3), z, evaluate=False)
    assert u.ap == Tuple(1, 2, 2)
    assert u.bq == Tuple(1, 1, 2, 3)

    h = hyper((1, 2), (3, 4, 5), z)
    assert h.ap == Tuple(1, 2)
    assert h.bq == Tuple(3, 4, 5)
    assert h.argument == z
    assert h.is_commutative is True
    h = hyper((2, 1), (4, 3, 5), z)
    assert h.ap == Tuple(1, 2)
    assert h.bq == Tuple(3, 4, 5)
    assert h.argument == z
    assert h.is_commutative is True

    # just a few checks to make sure that all arguments go where they should
    assert tn(hyper(Tuple(), Tuple(), z), exp(z), z)
    assert tn(z*hyper((1, 1), Tuple(2), -z), log(1 + z), z)

    # differentiation
    h = hyper(
        (randcplx(), randcplx(), randcplx()), (randcplx(), randcplx()), z)
    assert td(h, z)

    a1, a2, b1, b2, b3 = symbols('a1:3, b1:4')
    assert hyper((a1, a2), (b1, b2, b3), z).diff(z) == \
        a1*a2/(b1*b2*b3) * hyper((a1 + 1, a2 + 1), (b1 + 1, b2 + 1, b3 + 1), z)

    # differentiation wrt parameters is not supported
    assert hyper([z], [], z).diff(z) == Derivative(hyper([z], [], z), z)

    # hyper is unbranched wrt parameters
    from sympy.functions.elementary.complexes import polar_lift
    assert hyper([polar_lift(z)], [polar_lift(k)], polar_lift(x)) == \
        hyper([z], [k], polar_lift(x))

    # hyper does not automatically evaluate anyway, but the test is to make
    # sure that the evaluate keyword is accepted
    assert hyper((1, 2), (1,), z, evaluate=False).func is hyper

