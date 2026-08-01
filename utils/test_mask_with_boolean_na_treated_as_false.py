
def test_mask_with_boolean_na_treated_as_false(index):
    # https://github.com/pandas-dev/pandas/issues/31503
    ser = Series(range(3))
    idx = Categorical([True, False, None])
    if index:
        idx = CategoricalIndex(idx)

    result = ser[idx]
    expected = ser[idx.fillna(False)]

    tm.assert_series_equal(result, expected)

