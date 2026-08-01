
def test_normalized_gen_harmonic(typ, j, k, n, a, ref):
    h = _normalized_gen_harmonic(typ(j), typ(k), typ(n), a)
    assert_allclose(h, ref, 5e-15)

