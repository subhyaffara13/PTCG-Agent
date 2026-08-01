
def test_select_columns_in_where(temp_hdfstore):
    # GH 6169
    # recreate multi-indexes when columns is passed
    # in the `where` argument
    index = MultiIndex(
        levels=[["foo", "bar", "baz", "qux"], ["one", "two", "three"]],
        codes=[[0, 0, 0, 1, 1, 2, 2, 3, 3, 3], [0, 1, 2, 0, 1, 1, 2, 0, 1, 2]],
        names=["foo_name", "bar_name"],
    )

    # With a DataFrame
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 3)),
        index=index,
        columns=["A", "B", "C"],
    )

    temp_hdfstore.put("df", df, format="table")
    expected = df[["A"]]

    tm.assert_frame_equal(temp_hdfstore.select("df", columns=["A"]), expected)

    tm.assert_frame_equal(temp_hdfstore.select("df", where="columns=['A']"), expected)

    # With a Series
    s = Series(np.random.default_rng(2).standard_normal(10), index=index, name="A")
    temp_hdfstore.put("s", s, format="table")
    tm.assert_series_equal(temp_hdfstore.select("s", where="columns=['A']"), s)

