
def test_cut_nullable_integer(bins, right, include_lowest):
    a = np.random.default_rng(2).integers(0, 10, size=50).astype(float)
    a[::2] = np.nan
    b = a.astype(object)
    b[::2] = pd.NA
    result = cut(
        pd.array(b, dtype="Int64"), bins, right=right, include_lowest=include_lowest
    )
    expected = cut(a, bins, right=right, include_lowest=include_lowest)
    tm.assert_categorical_equal(result, expected)

