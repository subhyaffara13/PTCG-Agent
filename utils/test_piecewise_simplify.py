from typing import Tuple

def test_piecewise_simplify():
    p = Piecewise(((x**2 + 1)/x**2, Eq(x*(1 + x) - x**2, 0)),
                  ((-1)**x*(-1), True))
    assert p.simplify() == \
        Piecewise((zoo, Eq(x, 0)), ((-1)**(x + 1), True))
    # simplify when there are Eq in conditions
    assert Piecewise(
        (a, And(Eq(a, 0), Eq(a + b, 0))), (1, True)).simplify(
        ) == Piecewise(
        (0, And(Eq(a, 0), Eq(b, 0))), (1, True))
    assert Piecewise((2*x*factorial(a)/(factorial(y)*factorial(-y + a)),
        Eq(y, 0) & Eq(-y + a, 0)), (2*factorial(a)/(factorial(y)*factorial(-y
        + a)), Eq(y, 0) & Eq(-y + a, 1)), (0, True)).simplify(
        ) == Piecewise(
            (2*x, And(Eq(a, 0), Eq(y, 0))),
            (2, And(Eq(a, 1), Eq(y, 0))),
            (0, True))
    args = (2, And(Eq(x, 2), Ge(y, 0))), (x, True)
    assert Piecewise(*args).simplify() == Piecewise(*args)
    args = (1, Eq(x, 0)), (sin(x)/x, True)
    assert Piecewise(*args).simplify() == Piecewise(*args)
    assert Piecewise((2 + y, And(Eq(x, 2), Eq(y, 0))), (x, True)
        ).simplify() == x
    # check that x or f(x) are recognized as being Symbol-like for lhs
    args = Tuple((1, Eq(x, 0)), (sin(x) + 1 + x, True))
    ans = x + sin(x) + 1
    f = Function('f')
    assert Piecewise(*args).simplify() == ans
    assert Piecewise(*args.subs(x, f(x))).simplify() == ans.subs(x, f(x))

    # issue 18634
    d = Symbol("d", integer=True)
    n = Symbol("n", integer=True)
    t = Symbol("t", positive=True)
    expr = Piecewise((-d + 2*n, Eq(1/t, 1)), (t**(1 - 4*n)*t**(4*n - 1)*(-d + 2*n), True))
    assert expr.simplify() == -d + 2*n

    # issue 22747
    p = Piecewise((0, (t < -2) & (t < -1) & (t < 0)), ((t/2 + 1)*(t +
        1)*(t + 2), (t < -1) & (t < 0)), ((S.Half - t/2)*(1 - t)*(t + 1),
        (t < -2) & (t < -1) & (t < 1)), ((t + 1)*(-t*(t/2 + 1) + (S.Half
        - t/2)*(1 - t)), (t < -2) & (t < -1) & (t < 0) & (t < 1)), ((t +
        1)*((S.Half - t/2)*(1 - t) + (t/2 + 1)*(t + 2)), (t < -1) & (t <
        1)), ((t + 1)*(-t*(t/2 + 1) + (S.Half - t/2)*(1 - t)), (t < -1) &
        (t < 0) & (t < 1)), (0, (t < -2) & (t < -1)), ((t/2 + 1)*(t +
        1)*(t + 2), t < -1), ((t + 1)*(-t*(t/2 + 1) + (S.Half - t/2)*(t +
        1)), (t < 0) & ((t < -2) | (t < 0))), ((S.Half - t/2)*(1 - t)*(t
        + 1), (t < 1) & ((t < -2) | (t < 1))), (0, True)) + Piecewise((0,
        (t < -1) & (t < 0) & (t < 1)), ((1 - t)*(t/2 + S.Half)*(t + 1),
        (t < 0) & (t < 1)), ((1 - t)*(1 - t/2)*(2 - t), (t < -1) & (t <
        0) & (t < 2)), ((1 - t)*((1 - t)*(t/2 + S.Half) + (1 - t/2)*(2 -
        t)), (t < -1) & (t < 0) & (t < 1) & (t < 2)), ((1 - t)*((1 -
        t/2)*(2 - t) + (t/2 + S.Half)*(t + 1)), (t < 0) & (t < 2)), ((1 -
        t)*((1 - t)*(t/2 + S.Half) + (1 - t/2)*(2 - t)), (t < 0) & (t <
        1) & (t < 2)), (0, (t < -1) & (t < 0)), ((1 - t)*(t/2 +
        S.Half)*(t + 1), t < 0), ((1 - t)*(t*(1 - t/2) + (1 - t)*(t/2 +
        S.Half)), (t < 1) & ((t < -1) | (t < 1))), ((1 - t)*(1 - t/2)*(2
        - t), (t < 2) & ((t < -1) | (t < 2))), (0, True))
    assert p.simplify() == Piecewise(
        (0, t < -2), ((t + 1)*(t + 2)**2/2, t < -1), (-3*t**3/2
        - 5*t**2/2 + 1, t < 0), (3*t**3/2 - 5*t**2/2 + 1, t < 1), ((1 -
        t)*(t - 2)**2/2, t < 2), (0, True))

    # coverage
    nan = Undefined
    assert Piecewise((1, x > 3), (2, x < 2), (3, x > 1)).simplify(
        )  == Piecewise((1, x > 3), (2, x < 2), (3, True))
    assert Piecewise((1, x < 2), (2, x < 1), (3, True)).simplify(
        ) == Piecewise((1, x < 2), (3, True))
    assert Piecewise((1, x > 2)).simplify() == Piecewise((1, x > 2),
        (nan, True))
    assert Piecewise((1, (x >= 2) & (x < oo))
        ).simplify() == Piecewise((1, (x >= 2) & (x < oo)), (nan, True))
    assert Piecewise((1, x < 2), (2, (x > 1) & (x < 3)), (3, True)
        ). simplify() == Piecewise((1, x < 2), (2, x < 3), (3, True))
    assert Piecewise((1, x < 2), (2, (x <= 3) & (x > 1)), (3, True)
        ).simplify() == Piecewise((1, x < 2), (2, x <= 3), (3, True))
    assert Piecewise((1, x < 2), (2, (x > 2) & (x < 3)), (3, True)
        ).simplify() == Piecewise((1, x < 2), (2, (x > 2) & (x < 3)),
        (3, True))
    assert Piecewise((1, x < 2), (2, (x >= 1) & (x <= 3)), (3, True)
        ).simplify() == Piecewise((1, x < 2), (2, x <= 3), (3, True))
    assert Piecewise((1, x < 1), (2, (x >= 2) & (x <= 3)), (3, True)
        ).simplify() == Piecewise((1, x < 1), (2, (x >= 2) & (x <= 3)),
        (3, True))
    # https://github.com/sympy/sympy/issues/25603
    assert Piecewise((log(x), (x <= 5) & (x > 3)), (x, True)
        ).simplify() == Piecewise((log(x), (x <= 5) & (x > 3)), (x, True))

    assert Piecewise((1, (x >= 1) & (x < 3)), (2, (x > 2) & (x < 4))
        ).simplify() == Piecewise((1, (x >= 1) & (x < 3)), (
        2, (x >= 3) & (x < 4)), (nan, True))
    assert Piecewise((1, (x >= 1) & (x <= 3)), (2, (x > 2) & (x < 4))
        ).simplify() == Piecewise((1, (x >= 1) & (x <= 3)), (
        2, (x > 3) & (x < 4)), (nan, True))

    # involves a symbolic range so cset.inf fails
    L = Symbol('L', nonnegative=True)
    p = Piecewise((nan, x <= 0), (0, (x >= 0) & (L > x) & (L - x <= 0)),
        (x - L/2, (L > x) & (L - x <= 0)),
        (L/2 - x, (x >= 0) & (L > x)),
        (0, L > x), (nan, True))
    assert p.simplify() == Piecewise(
        (nan, x <= 0), (L/2 - x, L > x), (nan, True))
    assert p.subs(L, y).simplify() == Piecewise(
        (nan, x <= 0), (-x + y/2, x < Max(0, y)), (0, x < y), (nan, True))

