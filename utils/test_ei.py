
def test_ei():
    assert Ei(0) is S.NegativeInfinity
    assert Ei(oo) is S.Infinity
    assert Ei(-oo) is S.Zero

    assert tn_branch(Ei)
    assert mytd(Ei(x), exp(x)/x, x)
    assert mytn(Ei(x), Ei(x).rewrite(uppergamma),
                -uppergamma(0, x*polar_lift(-1)) - I*pi, x)
    assert mytn(Ei(x), Ei(x).rewrite(expint),
                -expint(1, x*polar_lift(-1)) - I*pi, x)
    assert Ei(x).rewrite(expint).rewrite(Ei) == Ei(x)
    assert Ei(x*exp_polar(2*I*pi)) == Ei(x) + 2*I*pi
    assert Ei(x*exp_polar(-2*I*pi)) == Ei(x) - 2*I*pi

    assert mytn(Ei(x), Ei(x).rewrite(Shi), Chi(x) + Shi(x), x)
    assert mytn(Ei(x*polar_lift(I)), Ei(x*polar_lift(I)).rewrite(Si),
                Ci(x) + I*Si(x) + I*pi/2, x)

    assert Ei(log(x)).rewrite(li) == li(x)
    assert Ei(2*log(x)).rewrite(li) == li(x**2)

    assert gruntz(Ei(x+exp(-x))*exp(-x)*x, x, oo) == 1

    assert Ei(x).series(x) == EulerGamma + log(x) + x + x**2/4 + \
        x**3/18 + x**4/96 + x**5/600 + O(x**6)
    assert Ei(x).series(x, 1, 3) == Ei(1) + E*(x - 1) + O((x - 1)**3, (x, 1))
    assert Ei(x).series(x, oo) == \
        (120/x**5 + 24/x**4 + 6/x**3 + 2/x**2 + 1/x + 1 + O(x**(-6), (x, oo)))*exp(x)/x
    assert Ei(x).series(x, -oo) == \
        (120/x**5 + 24/x**4 + 6/x**3 + 2/x**2 + 1/x + 1 + O(x**(-6), (x, -oo)))*exp(x)/x
    assert Ei(-x).series(x, oo) == \
        -((-120/x**5 + 24/x**4 - 6/x**3 + 2/x**2 - 1/x + 1 + O(x**(-6), (x, oo)))*exp(-x)/x)

    assert str(Ei(cos(2)).evalf(n=10)) == '-0.6760647401'
    raises(ArgumentIndexError, lambda: Ei(x).fdiff(2))


def test_ei():
    mp.dps = 15
    assert ei(0) == -inf
    assert ei(inf) == inf
    assert ei(-inf) == -0.0
    assert ei(20+70j).ae(6.1041351911152984397e6 - 2.7324109310519928872e6j)
    # tests for the asymptotic expansion
    # values checked with Mathematica ExpIntegralEi
    mp.dps = 50
    r = ei(20000)
    s = '3.8781962825045010930273870085501819470698476975019e+8681'
    assert str(r) == s
    r = ei(-200)
    s = '-6.8852261063076355977108174824557929738368086933303e-90'
    assert str(r) == s
    r =ei(20000 + 10*j)
    sre = '-3.255138234032069402493850638874410725961401274106e+8681'
    sim = '-2.1081929993474403520785942429469187647767369645423e+8681'
    assert str(r.real) == sre and str(r.imag) == sim
    mp.dps = 15
    # More asymptotic expansions
    assert chi(-10**6+100j).ae('1.3077239389562548386e+434288 + 7.6808956999707408158e+434287j')
    assert shi(-10**6+100j).ae('-1.3077239389562548386e+434288 - 7.6808956999707408158e+434287j')
    mp.dps = 15
    assert ei(10j).ae(-0.0454564330044553726+3.2291439210137706686j)
    assert ei(100j).ae(-0.0051488251426104921+3.1330217936839529126j)
    u = ei(fmul(10**20, j, exact=True))
    assert u.real.ae(-6.4525128526578084421345e-21, abs_eps=0, rel_eps=8*eps)
    assert u.imag.ae(pi)
    assert ei(-10j).ae(-0.0454564330044553726-3.2291439210137706686j)
    assert ei(-100j).ae(-0.0051488251426104921-3.1330217936839529126j)
    u = ei(fmul(-10**20, j, exact=True))
    assert u.real.ae(-6.4525128526578084421345e-21, abs_eps=0, rel_eps=8*eps)
    assert u.imag.ae(-pi)
    assert ei(10+10j).ae(-1576.1504265768517448+436.9192317011328140j)
    u = ei(-10+10j)
    assert u.real.ae(7.6698978415553488362543e-7, abs_eps=0, rel_eps=8*eps)
    assert u.imag.ae(3.141595611735621062025)

