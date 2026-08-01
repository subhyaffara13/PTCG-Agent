
def test_reset_index_empty_frame_with_datetime64_multiindex():
    # https://github.com/pandas-dev/pandas/issues/35606
    dti = pd.DatetimeIndex(["2020-07-20 00:00:00"], dtype="M8[ns]")
    idx = MultiIndex.from_product([dti, [3, 4]], names=["a", "b"])[:0]
    df = DataFrame(index=idx, columns=["c", "d"])
    result = df.reset_index()
    expected = DataFrame(
        columns=list("abcd"), index=RangeIndex(start=0, stop=0, step=1)
    )
    expected["a"] = expected["a"].astype("datetime64[ns]")
    expected["b"] = expected["b"].astype("int64")
    tm.assert_frame_equal(result, expected)

