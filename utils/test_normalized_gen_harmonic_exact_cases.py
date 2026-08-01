
def test_normalized_gen_harmonic_exact_cases(typ, j, k, n, a, ref):
    h = _normalized_gen_harmonic(typ(j), typ(k), typ(n), a)
    assert_equal(h, ref)

