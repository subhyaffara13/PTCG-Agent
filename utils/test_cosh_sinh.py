
def test_cosh_sinh():
    R, x, y = ring('x, y', QQ)
    ch, sh = rs_cosh_sinh(x, x, 9)
    assert ch == rs_cosh(x, x, 9)
    assert sh == rs_sinh(x, x, 9)
    ch, sh = rs_cosh_sinh(x + x*y, x, 5)
    assert ch == rs_cosh(x + x*y, x, 5)
    assert sh == rs_sinh(x + x*y, x, 5)

    # constant term in series
    c, s = rs_cosh_sinh(1 + x + x**2, x, 5)
    assert c == rs_cosh(1 + x + x**2, x, 5)
    assert s == rs_sinh(1 + x + x**2, x, 5)

    a = symbols('a')
    R, x, y = ring('x, y', QQ[sinh(a), cosh(a), a])
    ch, sh = rs_cosh_sinh(x + a, x, 5)
    assert ch == rs_cosh(x + a, x, 5)
    assert sh == rs_sinh(x + a, x, 5)
    R, x, y = ring('x, y', EX)
    ch, sh = rs_cosh_sinh(x + a, x, 5)
    assert ch == rs_cosh(x + a, x, 5)
    assert sh == rs_sinh(x + a, x, 5)

