
def test_concat_mismatched_categoricals_with_empty():
    # concat_compat behavior on series._values should match pd.concat on series
    ser1 = Series(["a", "b", "c"], dtype="category")
    ser2 = Series([], dtype="category")

    result = _concat.concat_compat([ser1._values, ser2._values])
    expected = pd.concat([ser1, ser2])._values
    tm.assert_numpy_array_equal(result, expected)

