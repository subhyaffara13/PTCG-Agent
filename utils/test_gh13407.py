
def test_gh13407():
    # gh-13407 reported that the message produced by `scipy.optimize.toms748`
    # when `rtol < eps` is incorrect, and also that toms748 is unusual in
    # accepting `rtol` as low as eps while other solvers raise at 4*eps. Check
    # that the error message has been corrected and that `rtol=eps` can produce
    # a lower function value than `rtol=4*eps`.
    def f(x):
        return x**3 - 2*x - 5

    xtol = 1e-300
    eps = np.finfo(float).eps
    x1 = zeros.toms748(f, 1e-10, 1e10, xtol=xtol, rtol=1*eps)
    f1 = f(x1)
    x4 = zeros.toms748(f, 1e-10, 1e10, xtol=xtol, rtol=4*eps)
    f4 = f(x4)
    assert f1 < f4

    # using old-style syntax to get exactly the same message
    message = fr"rtol too small \({eps/2:g} < {eps:g}\)"
    with pytest.raises(ValueError, match=message):
        zeros.toms748(f, 1e-10, 1e10, xtol=xtol, rtol=eps/2)

