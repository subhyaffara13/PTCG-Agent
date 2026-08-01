
def test_issue_4326():
    R, b, h = symbols('R b h')
    # It doesn't matter if we can do the integral.  Just make sure the result
    # doesn't contain nan.  This is really a test against _eval_interval.
    e = integrate(((h*(x - R + b))/b)*sqrt(R**2 - x**2), (x, R - b, R))
    assert not e.has(nan)
    # See that it evaluates
    assert not e.has(Integral)

