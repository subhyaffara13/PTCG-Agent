import re

def test_polygamma():
    assert polygamma(n, nan) is nan

    assert polygamma(0, oo) is oo
    assert polygamma(0, -oo) is oo
    assert polygamma(0, I*oo) is oo
    assert polygamma(0, -I*oo) is oo
    assert polygamma(1, oo) == 0
    assert polygamma(5, oo) == 0

    assert polygamma(0, -9) is zoo

    assert polygamma(0, -9) is zoo
    assert polygamma(0, -1) is zoo
    assert polygamma(Rational(3, 2), -1) is zoo

    assert polygamma(0, 0) is zoo

    assert polygamma(0, 1) == -EulerGamma
    assert polygamma(0, 7) == Rational(49, 20) - EulerGamma

    assert polygamma(1, 1) == pi**2/6
    assert polygamma(1, 2) == pi**2/6 - 1
    assert polygamma(1, 3) == pi**2/6 - Rational(5, 4)
    assert polygamma(3, 1) == pi**4 / 15
    assert polygamma(3, 5) == 6*(Rational(-22369, 20736) + pi**4/90)
    assert polygamma(5, 1) == 8 * pi**6 / 63

    assert polygamma(1, S.Half) == pi**2 / 2
    assert polygamma(2, S.Half) == -14*zeta(3)
    assert polygamma(11, S.Half) == 176896*pi**12

    def t(m, n):
        x = S(m)/n
        r = polygamma(0, x)
        if r.has(polygamma):
            return False
        return abs(polygamma(0, x.n()).n() - r.n()).n() < 1e-10
    assert t(1, 2)
    assert t(3, 2)
    assert t(-1, 2)
    assert t(1, 4)
    assert t(-3, 4)
    assert t(1, 3)
    assert t(4, 3)
    assert t(3, 4)
    assert t(2, 3)
    assert t(123, 5)

    assert polygamma(0, x).rewrite(zeta) == polygamma(0, x)
    assert polygamma(1, x).rewrite(zeta) == zeta(2, x)
    assert polygamma(2, x).rewrite(zeta) == -2*zeta(3, x)
    assert polygamma(I, 2).rewrite(zeta) == polygamma(I, 2)
    n1 = Symbol('n1')
    n2 = Symbol('n2', real=True)
    n3 = Symbol('n3', integer=True)
    n4 = Symbol('n4', positive=True)
    n5 = Symbol('n5', positive=True, integer=True)
    assert polygamma(n1, x).rewrite(zeta) == polygamma(n1, x)
    assert polygamma(n2, x).rewrite(zeta) == polygamma(n2, x)
    assert polygamma(n3, x).rewrite(zeta) == polygamma(n3, x)
    assert polygamma(n4, x).rewrite(zeta) == polygamma(n4, x)
    assert polygamma(n5, x).rewrite(zeta) == (-1)**(n5 + 1) * factorial(n5) * zeta(n5 + 1, x)

    assert polygamma(3, 7*x).diff(x) == 7*polygamma(4, 7*x)

    assert polygamma(0, x).rewrite(harmonic) == harmonic(x - 1) - EulerGamma
    assert polygamma(2, x).rewrite(harmonic) == 2*harmonic(x - 1, 3) - 2*zeta(3)
    ni = Symbol("n", integer=True)
    assert polygamma(ni, x).rewrite(harmonic) == (-1)**(ni + 1)*(-harmonic(x - 1, ni + 1)
                                                                 + zeta(ni + 1))*factorial(ni)

    # Polygamma of non-negative integer order is unbranched:
    k = Symbol('n', integer=True, nonnegative=True)
    assert polygamma(k, exp_polar(2*I*pi)*x) == polygamma(k, x)

    # but negative integers are branched!
    k = Symbol('n', integer=True)
    assert polygamma(k, exp_polar(2*I*pi)*x).args == (k, exp_polar(2*I*pi)*x)

    # Polygamma of order -1 is loggamma:
    assert polygamma(-1, x) == loggamma(x) - log(2*pi) / 2

    # But smaller orders are iterated integrals and don't have a special name
    assert polygamma(-2, x).func is polygamma

    # Test a bug
    assert polygamma(0, -x).expand(func=True) == polygamma(0, -x)

    assert polygamma(2, 2.5).is_positive == False
    assert polygamma(2, -2.5).is_positive == False
    assert polygamma(3, 2.5).is_positive == True
    assert polygamma(3, -2.5).is_positive is True
    assert polygamma(-2, -2.5).is_positive is None
    assert polygamma(-3, -2.5).is_positive is None

    assert polygamma(2, 2.5).is_negative == True
    assert polygamma(3, 2.5).is_negative == False
    assert polygamma(3, -2.5).is_negative == False
    assert polygamma(2, -2.5).is_negative is True
    assert polygamma(-2, -2.5).is_negative is None
    assert polygamma(-3, -2.5).is_negative is None

    assert polygamma(I, 2).is_positive is None
    assert polygamma(I, 3).is_negative is None

    # issue 17350
    assert (I*polygamma(I, pi)).as_real_imag() == \
           (-im(polygamma(I, pi)), re(polygamma(I, pi)))
    assert (tanh(polygamma(I, 1))).rewrite(exp) == \
           (exp(polygamma(I, 1)) - exp(-polygamma(I, 1)))/(exp(polygamma(I, 1)) + exp(-polygamma(I, 1)))
    assert (I / polygamma(I, 4)).rewrite(exp) == \
           I*exp(-I*atan(im(polygamma(I, 4))/re(polygamma(I, 4))))/Abs(polygamma(I, 4))

    # issue 12569
    assert unchanged(im, polygamma(0, I))
    assert polygamma(Symbol('a', positive=True), Symbol('b', positive=True)).is_real is True
    assert polygamma(0, I).is_real is None

    assert str(polygamma(pi, 3).evalf(n=10)) == "0.1169314564"
    assert str(polygamma(2.3, 1.0).evalf(n=10)) == "-3.003302909"
    assert str(polygamma(-1, 1).evalf(n=10)) == "-0.9189385332" # not zero
    assert str(polygamma(I, 1).evalf(n=10)) == "-3.109856569 + 1.89089016*I"
    assert str(polygamma(1, I).evalf(n=10)) == "-0.5369999034 - 0.7942335428*I"
    assert str(polygamma(I, I).evalf(n=10)) == "6.332362889 + 45.92828268*I"


def test_polygamma():
    mp.dps = 15
    psi0 = lambda z: psi(0,z)
    psi1 = lambda z: psi(1,z)
    assert psi0(3) == psi(0,3) == digamma(3)
    #assert psi2(3) == psi(2,3) == tetragamma(3)
    #assert psi3(3) == psi(3,3) == pentagamma(3)
    assert psi0(pi).ae(0.97721330794200673)
    assert psi0(-pi).ae(7.8859523853854902)
    assert psi0(-pi+1).ae(7.5676424992016996)
    assert psi0(pi+j).ae(1.04224048313859376 + 0.35853686544063749j)
    assert psi0(-pi-j).ae(1.3404026194821986 - 2.8824392476809402j)
    assert findroot(psi0, 1).ae(1.4616321449683622)
    assert psi0(1e-10).ae(-10000000000.57722)
    assert psi0(1e-40).ae(-1.000000000000000e+40)
    assert psi0(1e-10+1e-10j).ae(-5000000000.577215 + 5000000000.000000j)
    assert psi0(1e-40+1e-40j).ae(-5.000000000000000e+39 + 5.000000000000000e+39j)
    assert psi0(inf) == inf
    assert psi1(inf) == 0
    assert psi(2,inf) == 0
    assert psi1(pi).ae(0.37424376965420049)
    assert psi1(-pi).ae(53.030438740085385)
    assert psi1(pi+j).ae(0.32935710377142464 - 0.12222163911221135j)
    assert psi1(-pi-j).ae(-0.30065008356019703 + 0.01149892486928227j)
    assert (10**6*psi(4,1+10*pi*j)).ae(-6.1491803479004446 - 0.3921316371664063j)
    assert psi0(1+10*pi*j).ae(3.4473994217222650 + 1.5548808324857071j)
    assert isnan(psi0(nan))
    assert isnan(psi0(-inf))
    assert psi0(-100.5).ae(4.615124601338064)
    assert psi0(3+0j).ae(psi0(3))
    assert psi0(-100+3j).ae(4.6106071768714086321+3.1117510556817394626j)
    assert isnan(psi(2,mpc(0,inf)))
    assert isnan(psi(2,mpc(0,nan)))
    assert isnan(psi(2,mpc(0,-inf)))
    assert isnan(psi(2,mpc(1,inf)))
    assert isnan(psi(2,mpc(1,nan)))
    assert isnan(psi(2,mpc(1,-inf)))
    assert isnan(psi(2,mpc(inf,inf)))
    assert isnan(psi(2,mpc(nan,nan)))
    assert isnan(psi(2,mpc(-inf,-inf)))
    mp.dps = 30
    # issue #534
    assert digamma(-0.75+1j).ae(mpc('0.46317279488182026118963809283042317', '2.4821070143037957102007677817351115'))
    mp.dps = 15

