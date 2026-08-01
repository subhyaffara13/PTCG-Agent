
def test_15231():
    df = DataFrame([[1, 2], [3, 4]], columns=["a", "b"])
    df.loc[2] = Series({"a": 5, "b": 6})
    assert (df.dtypes == np.int64).all()

    df.loc[3] = Series({"a": 7})

    # df["a"] doesn't have any NaNs, should not have been cast
    exp_dtypes = Series([np.int64, np.float64], dtype=object, index=["a", "b"])
    tm.assert_series_equal(df.dtypes, exp_dtypes)

