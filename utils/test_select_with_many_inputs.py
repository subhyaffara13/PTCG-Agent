
def test_select_with_many_inputs(temp_hdfstore):
    df = DataFrame(
        {
            "ts": bdate_range("2012-01-01", periods=300, unit="ns"),
            "A": np.random.default_rng(2).standard_normal(300),
            "B": range(300),
            "users": ["a"] * 50
            + ["b"] * 50
            + ["c"] * 100
            + [f"a{i:03d}" for i in range(100)],
        }
    )
    temp_hdfstore.append("df", df, data_columns=["ts", "A", "B", "users"])

    # regular select
    result = temp_hdfstore.select("df", "ts>=Timestamp('2012-02-01')")
    expected = df[df.ts >= Timestamp("2012-02-01")]
    tm.assert_frame_equal(expected, result)

    # small selector
    result = temp_hdfstore.select(
        "df", "ts>=Timestamp('2012-02-01') & users=['a','b','c']"
    )
    expected = df[(df.ts >= Timestamp("2012-02-01")) & df.users.isin(["a", "b", "c"])]
    tm.assert_frame_equal(expected, result)

    # big selector along the columns
    selector = ["a", "b", "c"] + [f"a{i:03d}" for i in range(60)]
    result = temp_hdfstore.select(
        "df", "ts>=Timestamp('2012-02-01') and users=selector"
    )
    expected = df[(df.ts >= Timestamp("2012-02-01")) & df.users.isin(selector)]
    tm.assert_frame_equal(expected, result)

    selector = range(100, 200)
    result = temp_hdfstore.select("df", "B=selector")
    expected = df[df.B.isin(selector)]
    tm.assert_frame_equal(expected, result)
    assert len(result) == 100

    # big selector along the index
    selector = Index(df.ts[0:100].values)
    result = temp_hdfstore.select("df", "ts=selector")
    expected = df[df.ts.isin(selector.values)]
    tm.assert_frame_equal(expected, result)
    assert len(result) == 100

