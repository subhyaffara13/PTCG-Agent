
def test_binary_ufunc_drops_series_name(ufunc, sparse, arrays_for_binary_ufunc):
    # Drop the names when they differ.
    a1, a2 = arrays_for_binary_ufunc
    s1 = pd.Series(a1, name="a")
    s2 = pd.Series(a2, name="b")

    result = ufunc(s1, s2)
    assert result.name is None

