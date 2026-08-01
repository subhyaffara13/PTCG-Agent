
def test_cos_sin():
    R, x, y = ring('x, y', QQ)
    c, s = rs_cos_sin(x, x, 9)
    assert c == rs_cos(x, x, 9)
    assert s == rs_sin(x, x, 9)
    c, s = rs_cos_sin(x + x*y, x, 5)
    assert c == rs_cos(x + x*y, x, 5)
    assert s == rs_sin(x + x*y, x, 5)

    # constant term in series
    c, s = rs_cos_sin(1 + x + x**2, x, 5)
    assert c == rs_cos(1 + x + x**2, x, 5)
    assert s == rs_sin(1 + x + x**2, x, 5)

    a = symbols('a')
    R, x, y = ring('x, y', QQ[sin(a), cos(a), a])
    c, s = rs_cos_sin(x + a, x, 5)
    assert c == rs_cos(x + a, x, 5)
    assert s == rs_sin(x + a, x, 5)

    R, x, y = ring('x, y', EX)
    c, s = rs_cos_sin(x + a, x, 5)
    assert c == rs_cos(x + a, x, 5)
    assert s == rs_sin(x + a, x, 5)

