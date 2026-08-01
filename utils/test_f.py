
def test_f():
    f = Function("f")
    assert residue(f(x)/x**5, x, 0) == f(x).diff(x, 4).subs(x, 0)/24


def test_F():
    assert F(z, 0) == z
    assert F(0, m) == 0
    assert F(pi*i/2, m) == i*K(m)
    assert F(z, oo) == 0
    assert F(z, -oo) == 0

    assert F(-z, m) == -F(z, m)

    assert F(z, m).diff(z) == 1/sqrt(1 - m*sin(z)**2)
    assert F(z, m).diff(m) == E(z, m)/(2*m*(1 - m)) - F(z, m)/(2*m) - \
        sin(2*z)/(4*(1 - m)*sqrt(1 - m*sin(z)**2))
    r = randcplx()
    assert td(F(z, r), z)
    assert td(F(r, m), m)

    mi = Symbol('m', real=False)
    assert F(z, mi).conjugate() == F(z.conjugate(), mi.conjugate())
    mr = Symbol('m', negative=True)
    assert F(z, mr).conjugate() == F(z.conjugate(), mr)

    assert F(z, m).series(z) == \
        z + z**5*(3*m**2/40 - m/30) + m*z**3/6 + O(z**6)

    assert F(z, m).rewrite(Integral).dummy_eq(
        Integral(1/sqrt(1 - m*sin(t)**2), (t, 0, z)))


def test_f(fft_mode: FFT_MODE_TYPE, f):
    """Verify the frequency values property `f`."""
    SFT = ShortTimeFFT(np.ones(5), hop=4, fs=5, fft_mode=fft_mode,
                       scale_to='psd')
    xp_assert_equal(SFT.f, f)

