
def test_unstack_categorical():
    # GH11558 (example is taken from the original issue)
    df = DataFrame(
        {"a": range(10), "medium": ["A", "B"] * 5, "artist": list("XYXXY") * 2}
    )
    df["medium"] = df["medium"].astype("category")

    gcat = df.groupby(["artist", "medium"], observed=False)["a"].count().unstack()
    result = gcat.describe()

    exp_columns = CategoricalIndex(["A", "B"], ordered=False, name="medium")
    tm.assert_index_equal(result.columns, exp_columns)
    tm.assert_categorical_equal(result.columns.values, exp_columns.values)

    result = gcat["A"] + gcat["B"]
    expected = Series([6, 4], index=Index(["X", "Y"], name="artist"))
    tm.assert_series_equal(result, expected)

