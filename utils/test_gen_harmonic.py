
def test_gen_harmonic(typ, n, a, ref):
    h = _gen_harmonic(typ(n), a)
    assert_allclose(h, ref, rtol=5e-15)

