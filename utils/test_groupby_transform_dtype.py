
def test_groupby_transform_dtype():
    # GH 22243
    df = DataFrame({"a": [1], "val": [1.35]})

    result = df["val"].transform(lambda x: x.map(lambda y: f"+{y}"))
    expected1 = Series(["+1.35"], name="val")
    tm.assert_series_equal(result, expected1)

    result = df.groupby("a")["val"].transform(lambda x: x.map(lambda y: f"+{y}"))
    tm.assert_series_equal(result, expected1)

    result = df.groupby("a")["val"].transform(lambda x: x.map(lambda y: f"+({y})"))
    expected2 = Series(["+(1.35)"], name="val")
    tm.assert_series_equal(result, expected2)

    df["val"] = df["val"].astype(object)
    result = df.groupby("a")["val"].transform(lambda x: x.map(lambda y: f"+{y}"))
    tm.assert_series_equal(result, expected1)

