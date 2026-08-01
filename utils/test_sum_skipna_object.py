
def test_sum_skipna_object(skipna):
    # GH#15675
    df = DataFrame(
        {
            "val": ["a", "b", np.nan, "d", "e", "f", "g", "h", "i", "j"],
            "cat": ["A", "B"] * 5,
        }
    ).astype({"val": object})
    if skipna:
        expected = Series(
            ["aegi", "bdfhj"], index=pd.Index(["A", "B"], name="cat"), name="val"
        ).astype(object)
    else:
        expected = Series(
            [np.nan, "bdfhj"], index=pd.Index(["A", "B"], name="cat"), name="val"
        ).astype(object)
    result = df.groupby("cat")["val"].sum(skipna=skipna)
    tm.assert_series_equal(result, expected)

