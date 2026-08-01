
def test_index_unique2():
    # NaT, note this is excluded
    arr = [1370745748 + t for t in range(20)] + [NaT._value]
    idx = DatetimeIndex(arr * 3)
    tm.assert_index_equal(idx.unique(), DatetimeIndex(arr))
    assert idx.nunique() == 20
    assert idx.nunique(dropna=False) == 21

