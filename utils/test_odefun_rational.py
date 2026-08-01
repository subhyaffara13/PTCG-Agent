
def test_odefun_rational():
    mp.dps = 15
    # A rational function
    f = lambda t: 1/(1+mpf(t)**2)
    g = odefun(lambda x, y: [-2*x*y[0]**2], 0, [f(0)])
    assert f(2).ae(g(2)[0])

