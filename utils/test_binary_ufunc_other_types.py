
def test_binary_ufunc_other_types(type_):
    a = pd.Series([1, 2, 3], name="name")
    b = type_([3, 4, 5])

    result = np.add(a, b)
    expected = pd.Series(np.add(a.to_numpy(), b), name="name")
    tm.assert_series_equal(result, expected)

