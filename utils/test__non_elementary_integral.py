
def test_NonElementaryIntegral():
    assert isinstance(risch_integrate(exp(x**2), x), NonElementaryIntegral)
    assert isinstance(risch_integrate(x**x*log(x), x), NonElementaryIntegral)
    # Make sure methods of Integral still give back a NonElementaryIntegral
    assert isinstance(NonElementaryIntegral(x**x*t0, x).subs(t0, log(x)), NonElementaryIntegral)

