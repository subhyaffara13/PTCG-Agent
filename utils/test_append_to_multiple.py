
def test_append_to_multiple(temp_hdfstore):
    df1 = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    df2 = df1.copy().rename(columns="{}_2".format)
    df2["foo"] = "bar"
    df = concat([df1, df2], axis=1)

    # exceptions
    msg = "append_to_multiple requires a selector that is in passed dict"
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append_to_multiple(
            {"df1": ["A", "B"], "df2": None}, df, selector="df3"
        )

    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append_to_multiple({"df1": None, "df2": None}, df, selector="df3")

    msg = (
        "append_to_multiple must have a dictionary specified as the way to "
        "split the value"
    )
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append_to_multiple("df1", df, "df1")

    # regular operation
    temp_hdfstore.append_to_multiple(
        {"df1": ["A", "B"], "df2": None}, df, selector="df1"
    )
    result = temp_hdfstore.select_as_multiple(
        ["df1", "df2"], where=["A>0", "B>0"], selector="df1"
    )
    expected = df[(df.A > 0) & (df.B > 0)]
    tm.assert_frame_equal(result, expected)

