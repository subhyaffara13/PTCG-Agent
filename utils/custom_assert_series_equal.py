
def custom_assert_series_equal(left, right, *args, **kwargs):
    # NumPy doesn't handle an array of equal-length UserDicts.
    # The default assert_series_equal eventually does a
    # Series.values, which raises. We work around it by
    # converting the UserDicts to dicts.
    if left.dtype.name == "json":
        assert left.dtype == right.dtype
        left = pd.Series(
            JSONArray(left.values.astype(object)), index=left.index, name=left.name
        )
        right = pd.Series(
            JSONArray(right.values.astype(object)),
            index=right.index,
            name=right.name,
        )
    tm.assert_series_equal(left, right, *args, **kwargs)

