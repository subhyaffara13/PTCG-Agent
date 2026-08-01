
def test_conversion_to_mpmath():
    assert mpmath.mpmathify(Integer(1)) == mpmath.mpf(1)
    assert mpmath.mpmathify(S.Half) == mpmath.mpf(0.5)
    assert mpmath.mpmathify(Float('1.23', 15)) == mpmath.mpf('1.23')

    assert mpmath.mpmathify(I) == mpmath.mpc(1j)

    assert mpmath.mpmathify(1 + 2*I) == mpmath.mpc(1 + 2j)
    assert mpmath.mpmathify(1.0 + 2*I) == mpmath.mpc(1 + 2j)
    assert mpmath.mpmathify(1 + 2.0*I) == mpmath.mpc(1 + 2j)
    assert mpmath.mpmathify(1.0 + 2.0*I) == mpmath.mpc(1 + 2j)
    assert mpmath.mpmathify(S.Half + S.Half*I) == mpmath.mpc(0.5 + 0.5j)

    assert mpmath.mpmathify(2*I) == mpmath.mpc(2j)
    assert mpmath.mpmathify(2.0*I) == mpmath.mpc(2j)
    assert mpmath.mpmathify(S.Half*I) == mpmath.mpc(0.5j)

    mpmath.mp.dps = 100
    assert mpmath.mpmathify(pi.evalf(100) + pi.evalf(100)*I) == mpmath.pi + mpmath.pi*mpmath.j
    assert mpmath.mpmathify(pi.evalf(100)*I) == mpmath.pi*mpmath.j

