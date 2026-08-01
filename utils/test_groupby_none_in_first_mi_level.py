
def test_groupby_none_in_first_mi_level():
    # GH#47348
    arr = [[None, 1, 0, 1], [2, 3, 2, 3]]
    ser = Series(1, index=MultiIndex.from_arrays(arr, names=["a", "b"]))
    result = ser.groupby(level=[0, 1]).sum()
    expected = Series(
        [1, 2], MultiIndex.from_tuples([(0.0, 2), (1.0, 3)], names=["a", "b"])
    )
    tm.assert_series_equal(result, expected)

