
def test_polylog_expansion():
    assert polylog(s, 0) == 0
    assert polylog(s, 1) == zeta(s)
    assert polylog(s, -1) == -dirichlet_eta(s)
    assert polylog(s, exp_polar(I*pi*Rational(4, 3))) == polylog(s, exp(I*pi*Rational(4, 3)))
    assert polylog(s, exp_polar(I*pi)/3) == polylog(s, exp(I*pi)/3)

    assert myexpand(polylog(1, z), -log(1 - z))
    assert myexpand(polylog(0, z), z/(1 - z))
    assert myexpand(polylog(-1, z), z/(1 - z)**2)
    assert ((1-z)**3 * expand_func(polylog(-2, z))).simplify() == z*(1 + z)
    assert myexpand(polylog(-5, z), None)

