
def test_gen_harmonic_n_nan():
    h = _gen_harmonic(np.nan, 0.75)
    assert_equal(h, np.nan)

