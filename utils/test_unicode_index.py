
def test_unicode_index(temp_h5_path):
    unicode_values = ["\u03c3", "\u03c3\u03c3"]

    s = Series(
        np.random.default_rng(2).standard_normal(len(unicode_values)),
        unicode_values,
    )
    _check_roundtrip(s, tm.assert_series_equal, path=temp_h5_path)

