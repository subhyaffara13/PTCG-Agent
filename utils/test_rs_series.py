
def test_rs_series():
    x, a, b, c = symbols('x, a, b, c')

    assert rs_series(a, a, 5).as_expr() == a
    assert rs_series(sin(a), a, 5).as_expr() == (sin(a).series(a, 0,
        5)).removeO()
    assert rs_series(sin(a) + cos(a), a, 5).as_expr() == ((sin(a) +
        cos(a)).series(a, 0, 5)).removeO()
    assert rs_series(sin(a)*cos(a), a, 5).as_expr() == ((sin(a)*
        cos(a)).series(a, 0, 5)).removeO()

    p = (sin(a) - a)*(cos(a**2) + a**4/2)
    assert expand(rs_series(p, a, 10).as_expr()) == expand(p.series(a, 0,
        10).removeO())

    p = sin(a**2/2 + a/3) + cos(a/5)*sin(a/2)**3
    assert expand(rs_series(p, a, 5).as_expr()) == expand(p.series(a, 0,
        5).removeO())

    p = sin(x**2 + a)*(cos(x**3 - 1) - a - a**2)
    assert expand(rs_series(p, a, 5).as_expr()) == expand(p.series(a, 0,
        5).removeO())

    p = sin(a**2 - a/3 + 2)**5*exp(a**3 - a/2)
    assert expand(rs_series(p, a, 10).as_expr()) == expand(p.series(a, 0,
        10).removeO())

    p = sin(a + b + c)
    assert expand(rs_series(p, a, 5).as_expr()) == expand(p.series(a, 0,
        5).removeO())

    p = tan(sin(a**2 + 4) + b + c)
    assert expand(rs_series(p, a, 6).as_expr()) == expand(p.series(a, 0,
        6).removeO())

    p = a**QQ(2,5) + a**QQ(2,3) + a

    r = rs_series(tan(p), a, 2)
    assert r.as_expr() == a**QQ(9,5) + a**QQ(26,15) + a**QQ(22,15) + a**QQ(6,5)/3 + \
        a + a**QQ(2,3) + a**QQ(2,5)

    r = rs_series(exp(p), a, 1)
    assert r.as_expr() == a**QQ(4,5)/2 + a**QQ(2,3) + a**QQ(2,5) + 1

    r = rs_series(sin(p), a, 2)
    assert r.as_expr() == -a**QQ(9,5)/2 - a**QQ(26,15)/2 - a**QQ(22,15)/2 - \
        a**QQ(6,5)/6 + a + a**QQ(2,3) + a**QQ(2,5)

    r = rs_series(cos(p), a, 2)
    assert r.as_expr() == a**QQ(28,15)/6 - a**QQ(5,3) + a**QQ(8,5)/24 - a**QQ(7,5) - \
        a**QQ(4,3)/2 - a**QQ(16,15) - a**QQ(4,5)/2 + 1

    assert rs_series(sin(a)/7, a, 5).as_expr() == (sin(a)/7).series(a, 0,
            5).removeO()

