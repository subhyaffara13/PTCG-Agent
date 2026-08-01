
def test_polar():
    x, y = symbols('x y', polar=True)

    assert abs(exp_polar(I*4)) == 1
    assert abs(exp_polar(0)) == 1
    assert abs(exp_polar(2 + 3*I)) == exp(2)
    assert exp_polar(I*10).n() == exp_polar(I*10)

    assert log(exp_polar(z)) == z
    assert log(x*y).expand() == log(x) + log(y)
    assert log(x**z).expand() == z*log(x)

    assert exp_polar(3).exp == 3

    # Compare exp(1.0*pi*I).
    assert (exp_polar(1.0*pi*I).n(n=5)).as_real_imag()[1] >= 0

    assert exp_polar(0).is_rational is True  # issue 8008


def test_polar():
    from sympy.functions.elementary.complexes import polar_lift
    p = Symbol('p', polar=True)
    x = Symbol('x')
    assert p.is_polar
    assert x.is_polar is None
    assert S.One.is_polar is None
    assert (p**x).is_polar is True
    assert (x**p).is_polar is None
    assert ((2*p)**x).is_polar is True
    assert (2*p).is_polar is True
    assert (-2*p).is_polar is not True
    assert (polar_lift(-2)*p).is_polar is True

    q = Symbol('q', polar=True)
    assert (p*q)**2 == p**2 * q**2
    assert (2*q)**2 == 4 * q**2
    assert ((p*q)**x).expand() == p**x * q**x


def test_polar():
    plt.subplot(polar=True)
    fig = plt.gcf()
    pf = pickle.dumps(fig)
    pickle.loads(pf)
    plt.draw()

