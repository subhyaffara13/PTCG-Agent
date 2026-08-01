
def test_wavefunction():
    a = 1/Z
    R = {
        (1, 0): 2*sqrt(1/a**3) * exp(-r/a),
        (2, 0): sqrt(1/(2*a**3)) * exp(-r/(2*a)) * (1 - r/(2*a)),
        (2, 1): S.Half * sqrt(1/(6*a**3)) * exp(-r/(2*a)) * r/a,
        (3, 0): Rational(2, 3) * sqrt(1/(3*a**3)) * exp(-r/(3*a)) *
        (1 - 2*r/(3*a) + Rational(2, 27) * (r/a)**2),
        (3, 1): Rational(4, 27) * sqrt(2/(3*a**3)) * exp(-r/(3*a)) *
        (1 - r/(6*a)) * r/a,
        (3, 2): Rational(2, 81) * sqrt(2/(15*a**3)) * exp(-r/(3*a)) * (r/a)**2,
        (4, 0): Rational(1, 4) * sqrt(1/a**3) * exp(-r/(4*a)) *
        (1 - 3*r/(4*a) + Rational(1, 8) * (r/a)**2 - Rational(1, 192) * (r/a)**3),
        (4, 1): Rational(1, 16) * sqrt(5/(3*a**3)) * exp(-r/(4*a)) *
        (1 - r/(4*a) + Rational(1, 80) * (r/a)**2) * (r/a),
        (4, 2): Rational(1, 64) * sqrt(1/(5*a**3)) * exp(-r/(4*a)) *
        (1 - r/(12*a)) * (r/a)**2,
        (4, 3): Rational(1, 768) * sqrt(1/(35*a**3)) * exp(-r/(4*a)) * (r/a)**3,
    }
    for n, l in R:
        assert simplify(R_nl(n, l, r, Z) - R[(n, l)]) == 0


def test_wavefunction():
    Psi = {
        0: (1/sqrt(2 * pi)),
        1: (1/sqrt(2 * pi)) * exp(I * x),
        2: (1/sqrt(2 * pi)) * exp(2 * I * x),
        3: (1/sqrt(2 * pi)) * exp(3 * I * x)
    }
    for n in Psi:
        assert simplify(wavefunction(n, x) - Psi[n]) == 0


def test_wavefunction():
    Psi = {
        0: (nu/pi)**Rational(1, 4) * exp(-nu * x**2 /2),
        1: (nu/pi)**Rational(1, 4) * sqrt(2*nu) * x * exp(-nu * x**2 /2),
        2: (nu/pi)**Rational(1, 4) * (2 * nu * x**2 - 1)/sqrt(2) * exp(-nu * x**2 /2),
        3: (nu/pi)**Rational(1, 4) * sqrt(nu/3) * (2 * nu * x**3 - 3 * x) * exp(-nu * x**2 /2)
    }
    for n in Psi:
        assert simplify(psi_n(n, x, m, omega) - Psi[n]) == 0


def test_wavefunction():
    x, y = symbols('x y', real=True)
    L = symbols('L', positive=True)
    n = symbols('n', integer=True, positive=True)

    f = Wavefunction(x**2, x)
    p = f.prob()
    lims = f.limits

    assert f.is_normalized is False
    assert f.norm is oo
    assert f(10) == 100
    assert p(10) == 10000
    assert lims[x] == (-oo, oo)
    assert diff(f, x) == Wavefunction(2*x, x)
    raises(NotImplementedError, lambda: f.normalize())
    assert conjugate(f) == Wavefunction(conjugate(f.expr), x)
    assert conjugate(f) == Dagger(f)

    g = Wavefunction(x**2*y + y**2*x, (x, 0, 1), (y, 0, 2))
    lims_g = g.limits

    assert lims_g[x] == (0, 1)
    assert lims_g[y] == (0, 2)
    assert g.is_normalized is False
    assert g.norm == sqrt(42)/3
    assert g(2, 4) == 0
    assert g(1, 1) == 2
    assert diff(diff(g, x), y) == Wavefunction(2*x + 2*y, (x, 0, 1), (y, 0, 2))
    assert conjugate(g) == Wavefunction(conjugate(g.expr), *g.args[1:])
    assert conjugate(g) == Dagger(g)

    h = Wavefunction(sqrt(5)*x**2, (x, 0, 1))
    assert h.is_normalized is True
    assert h.normalize() == h
    assert conjugate(h) == Wavefunction(conjugate(h.expr), (x, 0, 1))
    assert conjugate(h) == Dagger(h)

    piab = Wavefunction(sin(n*pi*x/L), (x, 0, L))
    assert piab.norm == sqrt(L/2)
    assert piab(L + 1) == 0
    assert piab(0.5) == sin(0.5*n*pi/L)
    assert piab(0.5, n=1, L=1) == sin(0.5*pi)
    assert piab.normalize() == \
        Wavefunction(sqrt(2)/sqrt(L)*sin(n*pi*x/L), (x, 0, L))
    assert conjugate(piab) == Wavefunction(conjugate(piab.expr), (x, 0, L))
    assert conjugate(piab) == Dagger(piab)

    k = Wavefunction(x**2, 'x')
    assert type(k.variables[0]) == Symbol

