
def test_ci():
    m1 = exp_polar(I*pi)
    m1_ = exp_polar(-I*pi)
    pI = exp_polar(I*pi/2)
    mI = exp_polar(-I*pi/2)

    assert Ci(m1*x) == Ci(x) + I*pi
    assert Ci(m1_*x) == Ci(x) - I*pi
    assert Ci(pI*x) == Chi(x) + I*pi/2
    assert Ci(mI*x) == Chi(x) - I*pi/2
    assert Chi(m1*x) == Chi(x) + I*pi
    assert Chi(m1_*x) == Chi(x) - I*pi
    assert Chi(pI*x) == Ci(x) + I*pi/2
    assert Chi(mI*x) == Ci(x) - I*pi/2
    assert Ci(exp_polar(2*I*pi)*x) == Ci(x) + 2*I*pi
    assert Chi(exp_polar(-2*I*pi)*x) == Chi(x) - 2*I*pi
    assert Chi(exp_polar(2*I*pi)*x) == Chi(x) + 2*I*pi
    assert Ci(exp_polar(-2*I*pi)*x) == Ci(x) - 2*I*pi

    assert Ci(oo) is S.Zero
    assert Ci(-oo) == I*pi
    assert Chi(oo) is oo
    assert Chi(-oo) is oo

    assert mytd(Ci(x), cos(x)/x, x)
    assert mytd(Chi(x), cosh(x)/x, x)

    assert mytn(Ci(x), Ci(x).rewrite(Ei),
                Ei(x*exp_polar(-I*pi/2))/2 + Ei(x*exp_polar(I*pi/2))/2, x)
    assert mytn(Chi(x), Chi(x).rewrite(Ei),
                Ei(x)/2 + Ei(x*exp_polar(I*pi))/2 - I*pi/2, x)

    assert tn_arg(Ci)
    assert tn_arg(Chi)

    assert Ci(x).nseries(x, n=4) == \
        EulerGamma + log(x) - x**2/4 + O(x**4)
    assert Chi(x).nseries(x, n=4) == \
        EulerGamma + log(x) + x**2/4 + O(x**4)

    assert Ci(x).series(x, oo) == -cos(x)*(-6/x**4 + x**(-2) + O(x**(-6), (x, oo))) + \
        sin(x)*(24/x**5 - 2/x**3 + 1/x + O(x**(-6), (x, oo)))

    assert Ci(x).series(x, -oo) == -cos(x)*(-6/x**4 + x**(-2) + O(x**(-6), (x, -oo))) + \
        sin(x)*(24/x**5 - 2/x**3 + 1/x + O(x**(-6), (x, -oo))) + I*pi

    assert limit(log(x) - Ci(2*x), x, 0) == -log(2) - EulerGamma
    assert Ci(x).rewrite(uppergamma) == -expint(1, x*exp_polar(-I*pi/2))/2 -\
                                        expint(1, x*exp_polar(I*pi/2))/2
    assert Ci(x).rewrite(expint) == -expint(1, x*exp_polar(-I*pi/2))/2 -\
                                        expint(1, x*exp_polar(I*pi/2))/2
    raises(ArgumentIndexError, lambda: Ci(x).fdiff(2))

