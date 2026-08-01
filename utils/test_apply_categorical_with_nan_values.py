
def test_apply_categorical_with_nan_values(series, by_row):
    # GH 20714 bug fixed in: GH 24275
    s = Series(series, dtype="category")
    if not by_row:
        msg = "'Series' object has no attribute 'split'"
        with pytest.raises(AttributeError, match=msg):
            s.apply(lambda x: x.split("-")[0], by_row=by_row)
        return
    # NaN for cat dtype fixed in (GH 59966)
    result = s.apply(lambda x: x.split("-")[0] if pd.notna(x) else False, by_row=by_row)
    result = result.astype(object)
    expected = Series(["1", "1", False], dtype="category")
    expected = expected.astype(object)
    tm.assert_series_equal(result, expected)

