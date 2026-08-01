
def test_V14():
    r1 = integrate(log(abs(x**2 - y**2)), x)
    # Piecewise result does not simplify to the desired result.
    assert (r1.simplify() == x*log(abs(x**2  - y**2))
                            + y*log(x + y) - y*log(x - y) - 2*x)

