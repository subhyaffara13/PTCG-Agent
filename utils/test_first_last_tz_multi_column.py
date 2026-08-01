
def test_first_last_tz_multi_column(method, ts, alpha, unit):
    # GH 21603
    category_string = Series(list("abc")).astype("category")
    dti = pd.date_range("20130101", periods=3, tz="US/Eastern", unit=unit)
    df = DataFrame(
        {
            "group": [1, 1, 2],
            "category_string": category_string,
            "datetimetz": dti,
        }
    )
    result = getattr(df.groupby("group"), method)()
    expected = DataFrame(
        {
            "category_string": pd.Categorical(
                [alpha, "c"], dtype=category_string.dtype
            ),
            "datetimetz": [ts, Timestamp("2013-01-03", tz="US/Eastern")],
        },
        index=Index([1, 2], name="group"),
    )
    expected["datetimetz"] = expected["datetimetz"].dt.as_unit(unit)
    tm.assert_frame_equal(result, expected)

