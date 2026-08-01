
def test_integration_variable():
    raises(ValueError, lambda: Integral(exp(-x**2), 3))
    raises(ValueError, lambda: Integral(exp(-x**2), (3, -oo, oo)))

