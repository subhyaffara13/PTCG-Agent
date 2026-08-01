
def test_select(temp_hdfstore):
    # select with columns=
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )
    temp_hdfstore.append("df", df)
    result = temp_hdfstore.select("df", columns=["A", "B"])
    expected = df.reindex(columns=["A", "B"])
    tm.assert_frame_equal(expected, result)

    # equivalently
    result = temp_hdfstore.select("df", ["columns=['A', 'B']"])
    expected = df.reindex(columns=["A", "B"])
    tm.assert_frame_equal(expected, result)

    # with a data column
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df, data_columns=["A"])
    result = temp_hdfstore.select("df", ["A > 0"], columns=["A", "B"])
    expected = df[df.A > 0].reindex(columns=["A", "B"])
    tm.assert_frame_equal(expected, result)

    # all a data columns
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df, data_columns=True)
    result = temp_hdfstore.select("df", ["A > 0"], columns=["A", "B"])
    expected = df[df.A > 0].reindex(columns=["A", "B"])
    tm.assert_frame_equal(expected, result)

    # with a data column, but different columns
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df, data_columns=["A"])
    result = temp_hdfstore.select("df", ["A > 0"], columns=["C", "D"])
    expected = df[df.A > 0].reindex(columns=["C", "D"])
    tm.assert_frame_equal(expected, result)

