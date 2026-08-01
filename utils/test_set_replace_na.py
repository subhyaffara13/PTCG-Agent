
def test_set_replace_na(i):
    # Test strings of various lengths can be set to NaN and then replaced.
    s_empty = ""
    s_short = "0123456789"
    s_medium = "abcdefghijklmnopqrstuvwxyz"
    s_long = "-=+" * 100
    strings = [s_medium, s_empty, s_short, s_medium, s_long]
    a = np.array(strings, StringDType(na_object=np.nan))
    for s in [a[i], s_medium + s_short, s_short, s_empty, s_long]:
        a[i] = np.nan
        assert np.isnan(a[i])
        a[i] = s
        assert a[i] == s
        assert_array_equal(a, strings[:i] + [s] + strings[i + 1:])

