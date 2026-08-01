
def test_agg_cython_category_not_implemented_fallback():
    # https://github.com/pandas-dev/pandas/issues/31450
    df = DataFrame({"col_num": [1, 1, 2, 3]})
    df["col_cat"] = df["col_num"].astype("category")

    result = df.groupby("col_num").col_cat.first()

    # ordered categorical dtype should definitely be preserved;
    #  this is unordered, so is less-clear case (if anything, it should raise)
    expected = Series(
        [1, 2, 3],
        index=Index([1, 2, 3], name="col_num"),
        name="col_cat",
        dtype=df["col_cat"].dtype,
    )
    tm.assert_series_equal(result, expected)

    result = df.groupby("col_num").agg({"col_cat": "first"})
    expected = expected.to_frame()
    tm.assert_frame_equal(result, expected)

