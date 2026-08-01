
def test_principal_value():
    g = 1 / x
    assert Integral(g, (x, -oo, oo)).principal_value() == 0
    assert Integral(g, (y, -oo, oo)).principal_value() == oo * sign(1 / x)
    raises(ValueError, lambda: Integral(g, (x)).principal_value())
    raises(ValueError, lambda: Integral(g).principal_value())

    l = 1 / ((x ** 3) - 1)
    assert Integral(l, (x, -oo, oo)).principal_value().together() == -sqrt(3)*pi/3
    raises(ValueError, lambda: Integral(l, (x, -oo, 1)).principal_value())

    d = 1 / (x ** 2 - 1)
    assert Integral(d, (x, -oo, oo)).principal_value() == 0
    assert Integral(d, (x, -2, 2)).principal_value() == -log(3)

    v = x / (x ** 2 - 1)
    assert Integral(v, (x, -oo, oo)).principal_value() == 0
    assert Integral(v, (x, -2, 2)).principal_value() == 0

    s = x ** 2 / (x ** 2 - 1)
    assert Integral(s, (x, -oo, oo)).principal_value() is oo
    assert Integral(s, (x, -2, 2)).principal_value() == -log(3) + 4

    f = 1 / ((x ** 2 - 1) * (1 + x ** 2))
    assert Integral(f, (x, -oo, oo)).principal_value() == -pi / 2
    assert Integral(f, (x, -2, 2)).principal_value() == -atan(2) - log(3) / 2

