
def test_gh8904_zeroder_at_root_fails():
    """Test that Newton or Halley don't warn if zero derivative at root"""

    # a function that has a zero derivative at it's root
    def f_zeroder_root(x):
        return x**3 - x**2

    # should work with secant
    r = zeros.newton(f_zeroder_root, x0=0)
    assert_allclose(r, 0, atol=zeros._xtol, rtol=zeros._rtol)
    # test again with array
    r = zeros.newton(f_zeroder_root, x0=[0]*10)
    assert_allclose(r, 0, atol=zeros._xtol, rtol=zeros._rtol)

    # 1st derivative
    def fder(x):
        return 3 * x**2 - 2 * x

    # 2nd derivative
    def fder2(x):
        return 6*x - 2

    # should work with newton and halley
    r = zeros.newton(f_zeroder_root, x0=0, fprime=fder)
    assert_allclose(r, 0, atol=zeros._xtol, rtol=zeros._rtol)
    r = zeros.newton(f_zeroder_root, x0=0, fprime=fder,
                     fprime2=fder2)
    assert_allclose(r, 0, atol=zeros._xtol, rtol=zeros._rtol)
    # test again with array
    r = zeros.newton(f_zeroder_root, x0=[0]*10, fprime=fder)
    assert_allclose(r, 0, atol=zeros._xtol, rtol=zeros._rtol)
    r = zeros.newton(f_zeroder_root, x0=[0]*10, fprime=fder,
                     fprime2=fder2)
    assert_allclose(r, 0, atol=zeros._xtol, rtol=zeros._rtol)

    # also test that if a root is found we do not raise RuntimeWarning even if
    # the derivative is zero, EG: at x = 0.5, then fval = -0.125 and
    # fder = -0.25 so the next guess is 0.5 - (-0.125/-0.5) = 0 which is the
    # root, but if the solver continued with that guess, then it will calculate
    # a zero derivative, so it should return the root w/o RuntimeWarning
    r = zeros.newton(f_zeroder_root, x0=0.5, fprime=fder)
    assert_allclose(r, 0, atol=zeros._xtol, rtol=zeros._rtol)
    # test again with array
    r = zeros.newton(f_zeroder_root, x0=[0.5]*10, fprime=fder)
    assert_allclose(r, 0, atol=zeros._xtol, rtol=zeros._rtol)

