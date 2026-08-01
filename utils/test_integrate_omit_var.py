
def test_integrate_omit_var():
    y = Symbol('y')

    assert integrate(x) == x**2/2

    raises(ValueError, lambda: integrate(2))
    raises(ValueError, lambda: integrate(x*y))

