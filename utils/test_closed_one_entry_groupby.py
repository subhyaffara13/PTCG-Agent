
def test_closed_one_entry_groupby(func):
    # GH24718
    ser = DataFrame(
        data={"A": [1, 1, 2], "B": [3, 2, 1]},
        index=date_range("2000", periods=3),
    )
    result = getattr(
        ser.groupby("A", sort=False)["B"].rolling("10D", closed="left"), func
    )()
    exp_idx = MultiIndex.from_arrays(arrays=[[1, 1, 2], ser.index], names=("A", None))
    expected = Series(data=[np.nan, 3, np.nan], index=exp_idx, name="B")
    tm.assert_series_equal(result, expected)

