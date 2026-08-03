from typing import Tuple

def test_factor():
    f = x**5 - x**3 - x**2 + 1

    u = x + 1
    v = x - 1
    w = x**2 + x + 1

    F, U, V, W = map(Poly, (f, u, v, w))

    assert F.factor_list() == (1, [(U, 1), (V, 2), (W, 1)])
    assert factor_list(f) == (1, [(u, 1), (v, 2), (w, 1)])
    assert factor_list(f, x) == (1, [(u, 1), (v, 2), (w, 1)])
    assert factor_list(f, (x,)) == (1, [(u, 1), (v, 2), (w, 1)])
    assert factor_list(F) == (1, [(U, 1), (V, 2), (W, 1)])
    assert factor_list(f, polys=True) == (1, [(U, 1), (V, 2), (W, 1)])
    assert factor_list(F, polys=False) == (1, [(u, 1), (v, 2), (w, 1)])

    assert F.factor_list_include() == [(U, 1), (V, 2), (W, 1)]

    assert factor_list(1) == (1, [])
    assert factor_list(6) == (6, [])
    assert factor_list(sqrt(3), x) == (sqrt(3), [])
    assert factor_list((-1)**x, x) == (1, [(-1, x)])
    assert factor_list((2*x)**y, x) == (1, [(2, y), (x, y)])
    assert factor_list(sqrt(x*y), x) == (1, [(x*y, S.Half)])

    assert factor(6) == 6 and factor(6).is_Integer

    assert factor_list(3*x) == (3, [(x, 1)])
    assert factor_list(3*x**2) == (3, [(x, 2)])

    assert factor(3*x) == 3*x
    assert factor(3*x**2) == 3*x**2

    assert factor((2*x**2 + 2)**7) == 128*(x**2 + 1)**7

    assert factor(f) == u*v**2*w
    assert factor(f, x) == u*v**2*w
    assert factor(f, (x,)) == u*v**2*w

    g, p, q, r = x**2 - y**2, x - y, x + y, x**2 + 1

    assert factor(f/g) == (u*v**2*w)/(p*q)
    assert factor(f/g, x) == (u*v**2*w)/(p*q)
    assert factor(f/g, (x,)) == (u*v**2*w)/(p*q)

    p = Symbol('p', positive=True)
    i = Symbol('i', integer=True)
    r = Symbol('r', real=True)

    assert factor(sqrt(x*y)).is_Pow is True

    assert factor(sqrt(3*x**2 - 3)) == sqrt(3)*sqrt((x - 1)*(x + 1))
    assert factor(sqrt(3*x**2 + 3)) == sqrt(3)*sqrt(x**2 + 1)

    assert factor((y*x**2 - y)**i) == y**i*(x - 1)**i*(x + 1)**i
    assert factor((y*x**2 + y)**i) == y**i*(x**2 + 1)**i

    assert factor((y*x**2 - y)**t) == (y*(x - 1)*(x + 1))**t
    assert factor((y*x**2 + y)**t) == (y*(x**2 + 1))**t

    f = sqrt(expand((r**2 + 1)*(p + 1)*(p - 1)*(p - 2)**3))
    g = sqrt((p - 2)**3*(p - 1))*sqrt(p + 1)*sqrt(r**2 + 1)

    assert factor(f) == g
    assert factor(g) == g

    g = (x - 1)**5*(r**2 + 1)
    f = sqrt(expand(g))

    assert factor(f) == sqrt(g)

    f = Poly(sin(1)*x + 1, x, domain=EX)

    assert f.factor_list() == (1, [(f, 1)])

    f = x**4 + 1

    assert factor(f) == f
    assert factor(f, extension=I) == (x**2 - I)*(x**2 + I)
    assert factor(f, gaussian=True) == (x**2 - I)*(x**2 + I)
    assert factor(
        f, extension=sqrt(2)) == (x**2 + sqrt(2)*x + 1)*(x**2 - sqrt(2)*x + 1)

    assert factor(x**2 + 4*I*x - 4) == (x + 2*I)**2

    f = x**2 + 2*I*x - 4

    assert factor(f) == f

    f = 8192*x**2 + x*(22656 + 175232*I) - 921416 + 242313*I
    f_zzi = I*(x*(64 - 64*I) + 773 + 596*I)**2
    f_qqi = 8192*(x + S(177)/128 + 1369*I/128)**2

    assert factor(f) == f_zzi
    assert factor(f, domain=ZZ_I) == f_zzi
    assert factor(f, domain=QQ_I) == f_qqi

    f = x**2 + 2*sqrt(2)*x + 2

    assert factor(f, extension=sqrt(2)) == (x + sqrt(2))**2
    assert factor(f**3, extension=sqrt(2)) == (x + sqrt(2))**6

    assert factor(x**2 - 2*y**2, extension=sqrt(2)) == \
        (x + sqrt(2)*y)*(x - sqrt(2)*y)
    assert factor(2*x**2 - 4*y**2, extension=sqrt(2)) == \
        2*((x + sqrt(2)*y)*(x - sqrt(2)*y))

    assert factor(x - 1) == x - 1
    assert factor(-x - 1) == -x - 1

    assert factor(x - 1) == x - 1

    assert factor(6*x - 10) == Mul(2, 3*x - 5, evaluate=False)

    assert factor(x**11 + x + 1, modulus=65537, symmetric=True) == \
        (x**2 + x + 1)*(x**9 - x**8 + x**6 - x**5 + x**3 - x** 2 + 1)
    assert factor(x**11 + x + 1, modulus=65537, symmetric=False) == \
        (x**2 + x + 1)*(x**9 + 65536*x**8 + x**6 + 65536*x**5 +
         x**3 + 65536*x** 2 + 1)

    f = x/pi + x*sin(x)/pi
    g = y/(pi**2 + 2*pi + 1) + y*sin(x)/(pi**2 + 2*pi + 1)

    assert factor(f) == x*(sin(x) + 1)/pi
    assert factor(g) == y*(sin(x) + 1)/(pi + 1)**2

    assert factor(Eq(
        x**2 + 2*x + 1, x**3 + 1)) == Eq((x + 1)**2, (x + 1)*(x**2 - x + 1))

    f = (x**2 - 1)/(x**2 + 4*x + 4)

    assert factor(f) == (x + 1)*(x - 1)/(x + 2)**2
    assert factor(f, x) == (x + 1)*(x - 1)/(x + 2)**2

    f = 3 + x - x*(1 + x) + x**2

    assert factor(f) == 3
    assert factor(f, x) == 3

    assert factor(1/(x**2 + 2*x + 1/x) - 1) == -((1 - x + 2*x**2 +
                  x**3)/(1 + 2*x**2 + x**3))

    assert factor(f, expand=False) == f
    raises(PolynomialError, lambda: factor(f, x, expand=False))

    raises(FlagError, lambda: factor(x**2 - 1, polys=True))

    assert factor([x, Eq(x**2 - y**2, Tuple(x**2 - z**2, 1/x + 1/y))]) == \
        [x, Eq((x - y)*(x + y), Tuple((x - z)*(x + z), (x + y)/x/y))]

    assert not isinstance(
        Poly(x**3 + x + 1).factor_list()[1][0][0], PurePoly) is True
    assert isinstance(
        PurePoly(x**3 + x + 1).factor_list()[1][0][0], PurePoly) is True

    assert factor(sqrt(-x)) == sqrt(-x)

    # issue 5917
    e = (-2*x*(-x + 1)*(x - 1)*(-x*(-x + 1)*(x - 1) - x*(x - 1)**2)*(x**2*(x -
    1) - x*(x - 1) - x) - (-2*x**2*(x - 1)**2 - x*(-x + 1)*(-x*(-x + 1) +
    x*(x - 1)))*(x**2*(x - 1)**4 - x*(-x*(-x + 1)*(x - 1) - x*(x - 1)**2)))
    assert factor(e) == 0

    # deep option
    assert factor(sin(x**2 + x) + x, deep=True) == sin(x*(x + 1)) + x
    assert factor(sin(x**2 + x)*x, deep=True) == sin(x*(x + 1))*x

    assert factor(sqrt(x**2)) == sqrt(x**2)

    # issue 13149
    assert factor(expand((0.5*x+1)*(0.5*y+1))) == Mul(1.0, 0.5*x + 1.0,
        0.5*y + 1.0, evaluate = False)
    assert factor(expand((0.5*x+0.5)**2)) == 0.25*(1.0*x + 1.0)**2

    eq = x**2*y**2 + 11*x**2*y + 30*x**2 + 7*x*y**2 + 77*x*y + 210*x + 12*y**2 + 132*y + 360
    assert factor(eq, x) == (x + 3)*(x + 4)*(y**2 + 11*y + 30)
    assert factor(eq, x, deep=True) == (x + 3)*(x + 4)*(y**2 + 11*y + 30)
    assert factor(eq, y, deep=True) == (y + 5)*(y + 6)*(x**2 + 7*x + 12)

    # fraction option
    f = 5*x + 3*exp(2 - 7*x)
    assert factor(f, deep=True) == factor(f, deep=True, fraction=True)
    assert factor(f, deep=True, fraction=False) == 5*x + 3*exp(2)*exp(-7*x)

    assert factor_list(x**3 - x*y**2, t, w, x) == (
        1, [(x, 1), (x - y, 1), (x + y, 1)])
    assert factor_list((x+1)*(x**6-1)) == (
        1, [(x - 1, 1), (x + 1, 2), (x**2 - x + 1, 1), (x**2 + x + 1, 1)])

    # https://github.com/sympy/sympy/issues/24952
    s2, s2p, s2n = sqrt(2), 1 + sqrt(2), 1 - sqrt(2)
    pip, pin = 1 + pi, 1 - pi
    assert factor_list(s2p*s2n) == (-1, [(-s2n, 1), (s2p, 1)])
    assert factor_list(pip*pin) == (-1, [(-pin, 1), (pip, 1)])
    # Not sure about this one. Maybe coeff should be 1 or -1?
    assert factor_list(s2*s2n) == (-s2, [(-s2n, 1)])
    assert factor_list(pi*pin) == (-1, [(-pin, 1), (pi, 1)])
    assert factor_list(s2p*s2n, x) == (s2p*s2n, [])
    assert factor_list(pip*pin, x) == (pip*pin, [])
    assert factor_list(s2*s2n, x) == (s2*s2n, [])
    assert factor_list(pi*pin, x) == (pi*pin, [])
    assert factor_list((x - sqrt(2)*pi)*(x + sqrt(2)*pi), x) == (
        1, [(x - sqrt(2)*pi, 1), (x + sqrt(2)*pi, 1)])

    # https://github.com/sympy/sympy/issues/26497
    p = ((y - I)**2 * (y + I) * (x + 1))
    assert factor(expand(p)) == p

    p = ((x - I)**2 * (x + I) * (y + 1))
    assert factor(expand(p)) == p

    p = (y + 1)**2*(y + sqrt(2))**2*(x**2 + x + 2 + 3*sqrt(2))**2
    assert factor(expand(p), extension=True) == p

    e = (
        -x**2*y**4/(y**2 + 1) + 2*I*x**2*y**3/(y**2 + 1) + 2*I*x**2*y/(y**2 + 1) +
        x**2/(y**2 + 1) - 2*x*y**4/(y**2 + 1) + 4*I*x*y**3/(y**2 + 1) +
        4*I*x*y/(y**2 + 1) + 2*x/(y**2 + 1) - y**4 - y**4/(y**2 + 1) + 2*I*y**3
        + 2*I*y**3/(y**2 + 1) + 2*I*y + 2*I*y/(y**2 + 1) + 1 + 1/(y**2 + 1)
    )
    assert factor(e) == -(y - I)**3*(y + I)*(x**2 + 2*x + y**2 + 2)/(y**2 + 1)

    # issue 27506
    e = (I*t*x*y - 3*I*t - I*x*y*z - 6*x*y + 3*I*z + 18)
    assert factor(e) == -I*(x*y - 3)*(-t + z - 6*I)

    e = (8*x**2*z**2 - 32*x**2*z*t + 24*x**2*t**2 - 4*I*x*y*z**2 + 16*I*x*y*z*t -
         12*I*x*y*t**2 + z**4 - 8*z**3*t + 22*z**2*t**2 - 24*z*t**3 + 9*t**4)
    assert factor(e) == (-3*t + z)*(-t + z)*(3*t**2 - 4*t*z + 8*x**2 - 4*I*x*y + z**2)


def test_factor():
    assert factor(A*B - B*A) == A*B - B*A

