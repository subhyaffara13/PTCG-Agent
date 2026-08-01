
def test_lambdify_Derivative_zeta():
    # This is related to gh-11802 (and to lesser extent gh-26663)
    expr1 = zeta(x).diff(x, evaluate=False)
    f1 = lambdify(x, expr1, modules=['mpmath'])
    ans1 = f1(2)
    ref1 = (zeta(2+1e-8).evalf()-zeta(2).evalf())/1e-8
    assert abs(ans1 - ref1)/abs(ref1) < 1e-7

    expr2 = zeta(x**2).diff(x)
    f2 = lambdify(x, expr2, modules=['mpmath'])
    ans2 = f2(2**0.5)
    ref2 = 2*2**0.5*ref1
    assert abs(ans2-ref2)/abs(ref2) < 1e-7

