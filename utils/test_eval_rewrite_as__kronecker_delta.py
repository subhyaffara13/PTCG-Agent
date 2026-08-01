
def test_eval_rewrite_as_KroneckerDelta():
    x, y, z, n, t, m = symbols('x y z n t m')
    K = KroneckerDelta
    f = lambda p: expand(p.rewrite(K))

    p1 = Piecewise((0, Eq(x, y)), (1, True))
    assert f(p1) == 1 - K(x, y)

    p2 = Piecewise((x, Eq(y,0)), (z, Eq(t,0)), (n, True))
    assert f(p2) == n*K(0, t)*K(0, y) - n*K(0, t) - n*K(0, y) + n + \
           x*K(0, y) - z*K(0, t)*K(0, y) + z*K(0, t)

    p3 = Piecewise((1, Ne(x, y)), (0, True))
    assert f(p3) == 1 - K(x, y)

    p4 = Piecewise((1, Eq(x, 3)), (4, True), (5, True))
    assert f(p4) == 4 - 3*K(3, x)

    p5 = Piecewise((3, Ne(x, 2)), (4, Eq(y, 2)), (5, True))
    assert f(p5) == -K(2, x)*K(2, y) + 2*K(2, x) + 3

    p6 = Piecewise((0, Ne(x, 1) & Ne(y, 4)), (1, True))
    assert f(p6) == -K(1, x)*K(4, y) + K(1, x) + K(4, y)

    p7 = Piecewise((2, Eq(y, 3) & Ne(x, 2)), (1, True))
    assert f(p7) == -K(2, x)*K(3, y) + K(3, y) + 1

    p8 = Piecewise((4, Eq(x, 3) & Ne(y, 2)), (1, True))
    assert f(p8) == -3*K(2, y)*K(3, x) + 3*K(3, x) + 1

    p9 = Piecewise((6, Eq(x, 4) & Eq(y, 1)), (1, True))
    assert f(p9) == 5 * K(1, y) * K(4, x) + 1

    p10 = Piecewise((4, Ne(x, -4) | Ne(y, 1)), (1, True))
    assert f(p10) == -3 * K(-4, x) * K(1, y) + 4

    p11 = Piecewise((1, Eq(y, 2) | Ne(x, -3)), (2, True))
    assert f(p11) == -K(-3, x)*K(2, y) + K(-3, x) + 1

    p12 = Piecewise((-1, Eq(x, 1) | Ne(y, 3)), (1, True))
    assert f(p12) == -2*K(1, x)*K(3, y) + 2*K(3, y) - 1

    p13 = Piecewise((3, Eq(x, 2) | Eq(y, 4)), (1, True))
    assert f(p13) == -2*K(2, x)*K(4, y) + 2*K(2, x) + 2*K(4, y) + 1

    p14 = Piecewise((1, Ne(x, 0) | Ne(y, 1)), (3, True))
    assert f(p14) == 2 * K(0, x) * K(1, y) + 1

    p15 = Piecewise((2, Eq(x, 3) | Ne(y, 2)), (3, Eq(x, 4) & Eq(y, 5)), (1, True))
    assert f(p15) == -2*K(2, y)*K(3, x)*K(4, x)*K(5, y) + K(2, y)*K(3, x) + \
           2*K(2, y)*K(4, x)*K(5, y) - K(2, y) + 2

    p16 = Piecewise((0, Ne(m, n)), (1, True))*Piecewise((0, Ne(n, t)), (1, True))\
          *Piecewise((0, Ne(n, x)), (1, True)) - Piecewise((0, Ne(t, x)), (1, True))
    assert f(p16) == K(m, n)*K(n, t)*K(n, x) - K(t, x)

    p17 = Piecewise((0, Ne(t, x) & (Ne(m, n) | Ne(n, t) | Ne(n, x))),
                    (1, Ne(t, x)), (-1, Ne(m, n) | Ne(n, t) | Ne(n, x)), (0, True))
    assert f(p17) == K(m, n)*K(n, t)*K(n, x) - K(t, x)

    p18 = Piecewise((-4, Eq(y, 1) | (Eq(x, -5) & Eq(x, z))), (4, True))
    assert f(p18) == 8*K(-5, x)*K(1, y)*K(x, z) - 8*K(-5, x)*K(x, z) - 8*K(1, y) + 4

    p19 = Piecewise((0, x > 2), (1, True))
    assert f(p19) == p19

    p20 = Piecewise((0, And(x < 2, x > -5)), (1, True))
    assert f(p20) == p20

    p21 = Piecewise((0, Or(x > 1, x < 0)), (1, True))
    assert f(p21) == p21

    p22 = Piecewise((0, ~((Eq(y, -1) | Ne(x, 0)) & (Ne(x, 1) | Ne(y, -1)))), (1, True))
    assert f(p22) == K(-1, y)*K(0, x) - K(-1, y)*K(1, x) - K(0, x) + 1

