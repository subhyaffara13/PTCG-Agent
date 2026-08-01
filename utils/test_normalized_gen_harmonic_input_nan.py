
def test_normalized_gen_harmonic_input_nan():
    h = _normalized_gen_harmonic(1.0, np.nan, 10.0, 1.05)
    assert_equal(h, np.nan)

