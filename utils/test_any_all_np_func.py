
def test_any_all_np_func(func):
    # GH 20653
    df = DataFrame(
        [["foo", True], [np.nan, True], ["foo", True]], columns=["key", "val"]
    )

    exp = Series([True, np.nan, True], name="val")

    res = df.groupby("key")["val"].transform(func)
    tm.assert_series_equal(res, exp)

