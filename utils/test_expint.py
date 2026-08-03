import re

def test_expint():
    expr = Ei(x)
    string = 'Ei(x)'
    assert pretty(expr) == string
    assert upretty(expr) == string

    expr = expint(1, z)
    ucode_str = "E₁(z)"
    ascii_str = "expint(1, z)"
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    assert pretty(Shi(x)) == 'Shi(x)'
    assert pretty(Si(x)) == 'Si(x)'
    assert pretty(Ci(x)) == 'Ci(x)'
    assert pretty(Chi(x)) == 'Chi(x)'
    assert upretty(Shi(x)) == 'Shi(x)'
    assert upretty(Si(x)) == 'Si(x)'
    assert upretty(Ci(x)) == 'Ci(x)'
    assert upretty(Chi(x)) == 'Chi(x)'


def test_expint():
    x = Symbol('x')
    a = Symbol('a')
    u = Symbol('u', polar=True)

    # TODO LT of Si, Shi, Chi is a mess ...
    assert laplace_transform(Ci(x), x, s) == (-log(1 + s**2)/2/s, 0, True)
    assert (laplace_transform(expint(a, x), x, s, simplify=True) ==
            (lerchphi(s*exp_polar(I*pi), 1, a), 0, re(a) > S.Zero))
    assert (laplace_transform(expint(1, x), x, s, simplify=True) ==
            (log(s + 1)/s, 0, True))
    assert (laplace_transform(expint(2, x), x, s, simplify=True) ==
            ((s - log(s + 1))/s**2, 0, True))
    assert (inverse_laplace_transform(-log(1 + s**2)/2/s, s, u).expand() ==
            Heaviside(u)*Ci(u))
    assert (
        inverse_laplace_transform(log(s + 1)/s, s, x,
                                  simplify=True).rewrite(expint) ==
        Heaviside(x)*E1(x))
    assert (
        inverse_laplace_transform(
            (s - log(s + 1))/s**2, s, x,
            simplify=True).rewrite(expint).expand() ==
        (expint(2, x)*Heaviside(x)).rewrite(Ei).rewrite(expint).expand())


def test_expint():
    """ Test various exponential integrals. """
    from sympy.core.symbol import Symbol
    from sympy.functions.elementary.hyperbolic import sinh
    from sympy.functions.special.error_functions import (Chi, Ci, Ei, Shi, Si, expint)
    assert simplify(unpolarify(integrate(exp(-z*x)/x**y, (x, 1, oo),
                meijerg=True, conds='none'
                ).rewrite(expint).expand(func=True))) == expint(y, z)

    assert integrate(exp(-z*x)/x, (x, 1, oo), meijerg=True,
                     conds='none').rewrite(expint).expand() == \
        expint(1, z)
    assert integrate(exp(-z*x)/x**2, (x, 1, oo), meijerg=True,
                     conds='none').rewrite(expint).expand() == \
        expint(2, z).rewrite(Ei).rewrite(expint)
    assert integrate(exp(-z*x)/x**3, (x, 1, oo), meijerg=True,
                     conds='none').rewrite(expint).expand() == \
        expint(3, z).rewrite(Ei).rewrite(expint).expand()

    t = Symbol('t', positive=True)
    assert integrate(-cos(x)/x, (x, t, oo), meijerg=True).expand() == Ci(t)
    assert integrate(-sin(x)/x, (x, t, oo), meijerg=True).expand() == \
        Si(t) - pi/2
    assert integrate(sin(x)/x, (x, 0, z), meijerg=True) == Si(z)
    assert integrate(sinh(x)/x, (x, 0, z), meijerg=True) == Shi(z)
    assert integrate(exp(-x)/x, x, meijerg=True).expand().rewrite(expint) == \
        I*pi - expint(1, x)
    assert integrate(exp(-x)/x**2, x, meijerg=True).rewrite(expint).expand() \
        == expint(1, x) - exp(-x)/x - I*pi

    u = Symbol('u', polar=True)
    assert integrate(cos(u)/u, u, meijerg=True).expand().as_independent(u)[1] \
        == Ci(u)
    assert integrate(cosh(u)/u, u, meijerg=True).expand().as_independent(u)[1] \
        == Chi(u)

    assert integrate(expint(1, x), x, meijerg=True
            ).rewrite(expint).expand() == x*expint(1, x) - exp(-x)
    assert integrate(expint(2, x), x, meijerg=True
            ).rewrite(expint).expand() == \
        -x**2*expint(1, x)/2 + x*exp(-x)/2 - exp(-x)/2
    assert simplify(unpolarify(integrate(expint(y, x), x,
                 meijerg=True).rewrite(expint).expand(func=True))) == \
        -expint(y + 1, x)

    assert integrate(Si(x), x, meijerg=True) == x*Si(x) + cos(x)
    assert integrate(Ci(u), u, meijerg=True).expand() == u*Ci(u) - sin(u)
    assert integrate(Shi(x), x, meijerg=True) == x*Shi(x) - cosh(x)
    assert integrate(Chi(u), u, meijerg=True).expand() == u*Chi(u) - sinh(u)

    assert integrate(Si(x)*exp(-x), (x, 0, oo), meijerg=True) == pi/4
    assert integrate(expint(1, x)*sin(x), (x, 0, oo), meijerg=True) == log(2)/2


def test_expint():
    from sympy.functions.elementary.miscellaneous import Max
    from sympy.functions.special.error_functions import Ci, E1, Si
    from sympy.simplify.simplify import simplify

    aneg = Symbol('a', negative=True)
    u = Symbol('u', polar=True)

    assert mellin_transform(E1(x), x, s) == (gamma(s)/s, (0, oo), True)
    assert inverse_mellin_transform(gamma(s)/s, s, x,
              (0, oo)).rewrite(expint).expand() == E1(x)
    assert mellin_transform(expint(a, x), x, s) == \
        (gamma(s)/(a + s - 1), (Max(1 - re(a), 0), oo), True)
    # XXX IMT has hickups with complicated strips ...
    assert simplify(unpolarify(
                    inverse_mellin_transform(gamma(s)/(aneg + s - 1), s, x,
                  (1 - aneg, oo)).rewrite(expint).expand(func=True))) == \
        expint(aneg, x)

    assert mellin_transform(Si(x), x, s) == \
        (-2**s*sqrt(pi)*gamma(s/2 + S.Half)/(
        2*s*gamma(-s/2 + 1)), (-1, 0), True)
    assert inverse_mellin_transform(-2**s*sqrt(pi)*gamma((s + 1)/2)
                                    /(2*s*gamma(-s/2 + 1)), s, x, (-1, 0)) \
        == Si(x)

    assert mellin_transform(Ci(sqrt(x)), x, s) == \
        (-2**(2*s - 1)*sqrt(pi)*gamma(s)/(s*gamma(-s + S.Half)), (0, 1), True)
    assert inverse_mellin_transform(
        -4**s*sqrt(pi)*gamma(s)/(2*s*gamma(-s + S.Half)),
        s, u, (0, 1)).expand() == Ci(sqrt(u))


def test_expint():
    assert mytn(expint(x, y), expint(x, y).rewrite(uppergamma),
                y**(x - 1)*uppergamma(1 - x, y), x)
    assert mytd(
        expint(x, y), -y**(x - 1)*meijerg([], [1, 1], [0, 0, 1 - x], [], y), x)
    assert mytd(expint(x, y), -expint(x - 1, y), y)
    assert mytn(expint(1, x), expint(1, x).rewrite(Ei),
                -Ei(x*polar_lift(-1)) + I*pi, x)

    assert expint(-4, x) == exp(-x)/x + 4*exp(-x)/x**2 + 12*exp(-x)/x**3 \
        + 24*exp(-x)/x**4 + 24*exp(-x)/x**5
    assert expint(Rational(-3, 2), x) == \
        exp(-x)/x + 3*exp(-x)/(2*x**2) + 3*sqrt(pi)*erfc(sqrt(x))/(4*x**S('5/2'))

    assert tn_branch(expint, 1)
    assert tn_branch(expint, 2)
    assert tn_branch(expint, 3)
    assert tn_branch(expint, 1.7)
    assert tn_branch(expint, pi)

    assert expint(y, x*exp_polar(2*I*pi)) == \
        x**(y - 1)*(exp(2*I*pi*y) - 1)*gamma(-y + 1) + expint(y, x)
    assert expint(y, x*exp_polar(-2*I*pi)) == \
        x**(y - 1)*(exp(-2*I*pi*y) - 1)*gamma(-y + 1) + expint(y, x)
    assert expint(2, x*exp_polar(2*I*pi)) == 2*I*pi*x + expint(2, x)
    assert expint(2, x*exp_polar(-2*I*pi)) == -2*I*pi*x + expint(2, x)
    assert expint(1, x).rewrite(Ei).rewrite(expint) == expint(1, x)
    assert expint(x, y).rewrite(Ei) == expint(x, y)
    assert expint(x, y).rewrite(Ci) == expint(x, y)

    assert mytn(E1(x), E1(x).rewrite(Shi), Shi(x) - Chi(x), x)
    assert mytn(E1(polar_lift(I)*x), E1(polar_lift(I)*x).rewrite(Si),
                -Ci(x) + I*Si(x) - I*pi/2, x)

    assert mytn(expint(2, x), expint(2, x).rewrite(Ei).rewrite(expint),
                -x*E1(x) + exp(-x), x)
    assert mytn(expint(3, x), expint(3, x).rewrite(Ei).rewrite(expint),
                x**2*E1(x)/2 + (1 - x)*exp(-x)/2, x)

    assert expint(Rational(3, 2), z).nseries(z) == \
        2 + 2*z - z**2/3 + z**3/15 - z**4/84 + z**5/540 - \
        2*sqrt(pi)*sqrt(z) + O(z**6)

    assert E1(z).series(z) == -EulerGamma - log(z) + z - \
        z**2/4 + z**3/18 - z**4/96 + z**5/600 + O(z**6)

    assert expint(4, z).series(z) == Rational(1, 3) - z/2 + z**2/2 + \
        z**3*(log(z)/6 - Rational(11, 36) + EulerGamma/6 - I*pi/6) - z**4/24 + \
        z**5/240 + O(z**6)

    assert expint(n, x).series(x, oo, n=3) == \
        (n*(n + 1)/x**2 - n/x + 1 + O(x**(-3), (x, oo)))*exp(-x)/x

    assert expint(z, y).series(z, 0, 2) == exp(-y)/y - z*meijerg(((), (1, 1)),
                                  ((0, 0, 1), ()), y)/y + O(z**2)
    raises(ArgumentIndexError, lambda: expint(x, y).fdiff(3))

    neg = Symbol('neg', negative=True)
    assert Ei(neg).rewrite(Si) == Shi(neg) + Chi(neg) - I*pi


def test_expint():
    mp.dps = 15
    assert expint(0,0) == inf
    assert expint(0,1).ae(1/e)
    assert expint(0,1.5).ae(2/exp(1.5)/3)
    assert expint(1,1).ae(-ei(-1))
    assert expint(2,0).ae(1)
    assert expint(3,0).ae(1/2.)
    assert expint(4,0).ae(1/3.)
    assert expint(-2, 0.5).ae(26/sqrt(e))
    assert expint(-1,-1) == 0
    assert expint(-2,-1).ae(-e)
    assert expint(5.5, 0).ae(2/9.)
    assert expint(2.00000001,0).ae(100000000./100000001)
    assert expint(2+3j,4-j).ae(0.0023461179581675065414+0.0020395540604713669262j)
    assert expint('1.01', '1e-1000').ae(99.9999999899412802)
    assert expint('1.000000000001', 3.5).ae(0.00697013985754701819446)
    assert expint(2,3).ae(3*ei(-3)+exp(-3))
    assert (expint(10,20)*10**10).ae(0.694439055541231353)
    assert expint(3,inf) == 0
    assert expint(3.2,inf) == 0
    assert expint(3.2+2j,inf) == 0
    assert expint(1,3j).ae(-0.11962978600800032763 + 0.27785620120457163717j)
    assert expint(1,3).ae(0.013048381094197037413)
    assert expint(1,-3).ae(-ei(3)-pi*j)
    #assert expint(3) == expint(1,3)
    assert expint(1,-20).ae(-25615652.66405658882 - 3.1415926535897932385j)
    assert expint(1000000,0).ae(1./999999)
    assert expint(0,2+3j).ae(-0.025019798357114678171 + 0.027980439405104419040j)
    assert expint(-1,2+3j).ae(-0.022411973626262070419 + 0.038058922011377716932j)
    assert expint(-1.5,0) == inf

