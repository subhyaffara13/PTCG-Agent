
def test_double_integral():
    if numpy and not scipy:
        skip("scipy not installed.")
    # example from http://mpmath.org/doc/current/calculus/integration.html
    i = Integral(1/(1 - x**2*y**2), (x, 0, 1), (y, 0, z))
    l = lambdify([z], i)
    d = l(1)
    assert 1.23370055 < d < 1.233700551

