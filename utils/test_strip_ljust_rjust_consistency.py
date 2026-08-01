
def test_strip_ljust_rjust_consistency(string_array, unicode_array):
    rjs = np.char.rjust(string_array, 1000)
    rju = np.char.rjust(unicode_array, 1000)

    ljs = np.char.ljust(string_array, 1000)
    lju = np.char.ljust(unicode_array, 1000)

    assert_array_equal(
        np.char.lstrip(rjs),
        np.char.lstrip(rju).astype(StringDType()),
    )

    assert_array_equal(
        np.char.rstrip(ljs),
        np.char.rstrip(lju).astype(StringDType()),
    )

    assert_array_equal(
        np.char.strip(ljs),
        np.char.strip(lju).astype(StringDType()),
    )

    assert_array_equal(
        np.char.strip(rjs),
        np.char.strip(rju).astype(StringDType()),
    )

