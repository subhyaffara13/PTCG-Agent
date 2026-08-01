
def test_issue_5227():
    f = 0.0032513612725229*Piecewise((0, x < -80.8461538461539),
        (-0.0160799238820171*x + 1.33215984776403, x < 2),
        (Piecewise((0.3, x > 123), (0.7, True)) +
        Piecewise((0.4, x > 2), (0.6, True)), x <=
        123), (-0.00817409766454352*x + 2.10541401273885, x <
        380.571428571429), (0, True))
    i = integrate(f, (x, -oo, oo))
    assert i == Integral(f, (x, -oo, oo)).doit()
    assert str(i) == '1.00195081676351'
    assert Piecewise((1, x - y < 0), (0, True)
        ).integrate(y) == Piecewise((0, y <= x), (-x + y, True))

