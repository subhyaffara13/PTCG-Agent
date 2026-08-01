
def test_try_parse_dates():
    arr = np.array(["5/1/2000", "6/1/2000", "7/1/2000"], dtype=object)
    result = parsing.try_parse_dates(arr, parser=lambda x: du_parse(x, dayfirst=True))

    expected = np.array([du_parse(d, dayfirst=True) for d in arr])
    tm.assert_numpy_array_equal(result, expected)

