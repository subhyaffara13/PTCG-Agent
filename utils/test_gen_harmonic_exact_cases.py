
def test_gen_harmonic_exact_cases(typ, n, a, ref):
    h = _gen_harmonic(typ(n), a)
    assert_equal(h, ref)

