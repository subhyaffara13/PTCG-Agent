
def test_issue_6077():
    assert x**2.0/x == x**1.0
    assert x/x**2.0 == x**-1.0
    assert x*x**2.0 == x**3.0
    assert x**1.5*x**2.5 == x**4.0

    assert 2**(2.0*x)/2**x == 2**(1.0*x)
    assert 2**x/2**(2.0*x) == 2**(-1.0*x)
    assert 2**x*2**(2.0*x) == 2**(3.0*x)
    assert 2**(1.5*x)*2**(2.5*x) == 2**(4.0*x)

