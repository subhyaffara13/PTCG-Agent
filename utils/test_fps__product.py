
def test_fps__product():
    f1, f2, f3 = fps(sin(x)), fps(exp(x)), fps(cos(x))

    raises(ValueError, lambda: f1.product(exp(x), x))
    raises(ValueError, lambda: f1.product(fps(exp(x), dir=-1), x, 4))
    raises(ValueError, lambda: f1.product(fps(exp(x), x0=1), x, 4))
    raises(ValueError, lambda: f1.product(fps(exp(y)), x, 4))

    fprod = f1.product(f2, x)
    assert isinstance(fprod, FormalPowerSeriesProduct)
    assert isinstance(fprod.ffps, FormalPowerSeries)
    assert isinstance(fprod.gfps, FormalPowerSeries)
    assert fprod.f == sin(x)
    assert fprod.g == exp(x)
    assert fprod.function == sin(x) * exp(x)
    assert fprod._eval_terms(4) == x + x**2 + x**3/3
    assert fprod.truncate(4) == x + x**2 + x**3/3 + O(x**4)
    assert fprod.polynomial(4) == x + x**2 + x**3/3

    raises(NotImplementedError, lambda: fprod._eval_term(5))
    raises(NotImplementedError, lambda: fprod.infinite)
    raises(NotImplementedError, lambda: fprod._eval_derivative(x))
    raises(NotImplementedError, lambda: fprod.integrate(x))

    assert f1.product(f3, x)._eval_terms(4) == x - 2*x**3/3
    assert f1.product(f3, x).truncate(4) == x - 2*x**3/3 + O(x**4)

