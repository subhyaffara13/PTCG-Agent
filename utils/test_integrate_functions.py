
def test_integrate_functions():
    # issue 4111
    assert integrate(f(x), x) == Integral(f(x), x)
    assert integrate(f(x), (x, 0, 1)) == Integral(f(x), (x, 0, 1))
    assert integrate(f(x)*diff(f(x), x), x) == f(x)**2/2
    assert integrate(diff(f(x), x) / f(x), x) == log(f(x))

