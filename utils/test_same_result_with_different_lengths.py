
def test_same_result_with_different_lengths(method):
    # GH-54380
    len_smaller = 10
    len_bigger = 12
    window_size = 8

    rng = np.random.default_rng(2)
    data = rng.normal(loc=0.0, scale=1e3, size=len_bigger)
    window_smaller = Series(data[:len_smaller]).rolling(window_size)
    window_bigger = Series(data).rolling(window_size)

    result_smaller = getattr(window_smaller, method)()
    result_bigger = getattr(window_bigger, method)()

    result_bigger_trimmed = result_bigger[:len_smaller]

    tm.assert_series_equal(result_smaller, result_bigger_trimmed, check_exact=True)

