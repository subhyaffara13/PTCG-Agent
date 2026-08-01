
def test_fail_holzer():
    eq = lambda x, y, z: a*x**2 + b*y**2 - c*z**2
    a, b, c = 4, 79, 23
    x, y, z = xyz = 26, 1, 11
    X, Y, Z = ans = 2, 7, 13
    assert eq(*xyz) == 0
    assert eq(*ans) == 0
    assert max(a*x**2, b*y**2, c*z**2) <= a*b*c
    assert max(a*X**2, b*Y**2, c*Z**2) <= a*b*c
    h = holzer(x, y, z, a, b, c)
    assert h == ans  # it would be nice to get the smaller soln

