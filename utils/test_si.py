
def test_si():
    assert Si(I*x) == I*Shi(x)
    assert Shi(I*x) == I*Si(x)
    assert Si(-I*x) == -I*Shi(x)
    assert Shi(-I*x) == -I*Si(x)
    assert Si(-x) == -Si(x)
    assert Shi(-x) == -Shi(x)
    assert Si(exp_polar(2*pi*I)*x) == Si(x)
    assert Si(exp_polar(-2*pi*I)*x) == Si(x)
    assert Shi(exp_polar(2*pi*I)*x) == Shi(x)
    assert Shi(exp_polar(-2*pi*I)*x) == Shi(x)

    assert Si(oo) == pi/2
    assert Si(-oo) == -pi/2
    assert Shi(oo) is oo
    assert Shi(-oo) is -oo

    assert mytd(Si(x), sin(x)/x, x)
    assert mytd(Shi(x), sinh(x)/x, x)

    assert mytn(Si(x), Si(x).rewrite(Ei),
                -I*(-Ei(x*exp_polar(-I*pi/2))/2
               + Ei(x*exp_polar(I*pi/2))/2 - I*pi) + pi/2, x)
    assert mytn(Si(x), Si(x).rewrite(expint),
                -I*(-expint(1, x*exp_polar(-I*pi/2))/2 +
                    expint(1, x*exp_polar(I*pi/2))/2) + pi/2, x)
    assert mytn(Shi(x), Shi(x).rewrite(Ei),
                Ei(x)/2 - Ei(x*exp_polar(I*pi))/2 + I*pi/2, x)
    assert mytn(Shi(x), Shi(x).rewrite(expint),
                expint(1, x)/2 - expint(1, x*exp_polar(I*pi))/2 - I*pi/2, x)

    assert tn_arg(Si)
    assert tn_arg(Shi)

    assert Si(x)._eval_as_leading_term(x, None, 1) == x
    assert Si(2*x)._eval_as_leading_term(x, None, 1) == 2*x
    assert Si(sin(x))._eval_as_leading_term(x, None, 1) == x
    assert Si(x + 1)._eval_as_leading_term(x, None, 1) == Si(1)
    assert Si(1/x)._eval_as_leading_term(x, None, 1) == \
        Si(1/x)._eval_as_leading_term(x, None, -1) == Si(1/x)

    assert Si(x).nseries(x, n=8) == \
        x - x**3/18 + x**5/600 - x**7/35280 + O(x**8)
    assert Shi(x).nseries(x, n=8) == \
        x + x**3/18 + x**5/600 + x**7/35280 + O(x**8)
    assert Si(sin(x)).nseries(x, n=5) == x - 2*x**3/9 + O(x**5)
    assert Si(x).nseries(x, 1, n=3) == \
        Si(1) + (x - 1)*sin(1) + (x - 1)**2*(-sin(1)/2 + cos(1)/2) + O((x - 1)**3, (x, 1))

    assert Si(x).series(x, oo) == -sin(x)*(-6/x**4 + x**(-2) + O(x**(-6), (x, oo))) - \
        cos(x)*(24/x**5 - 2/x**3 + 1/x + O(x**(-6), (x, oo))) + pi/2

    t = Symbol('t', Dummy=True)
    assert Si(x).rewrite(sinc).dummy_eq(Integral(sinc(t), (t, 0, x)))

    assert limit(Shi(x), x, S.Infinity) == S.Infinity
    assert limit(Shi(x), x, S.NegativeInfinity) == S.NegativeInfinity

