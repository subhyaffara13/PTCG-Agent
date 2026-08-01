
def test_risch_integrate_float():
    assert risch_integrate((-60*exp(x) - 19.2*exp(4*x))*exp(4*x), x) == -2.4*exp(8*x) - 12.0*exp(5*x)

