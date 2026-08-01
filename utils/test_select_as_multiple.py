
def test_select_as_multiple(temp_hdfstore):
    df1 = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )
    df2 = df1.copy().rename(columns="{}_2".format)
    df2["foo"] = "bar"

    msg = "keys must be a list/tuple"
    # no tables stored
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.select_as_multiple(None, where=["A>0", "B>0"], selector="df1")

    temp_hdfstore.append("df1", df1, data_columns=["A", "B"])
    temp_hdfstore.append("df2", df2)

    # exceptions
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.select_as_multiple(None, where=["A>0", "B>0"], selector="df1")

    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.select_as_multiple([None], where=["A>0", "B>0"], selector="df1")

    msg = "'No object named df3 in the file'"
    with pytest.raises(KeyError, match=msg):
        temp_hdfstore.select_as_multiple(
            ["df1", "df3"], where=["A>0", "B>0"], selector="df1"
        )

    with pytest.raises(KeyError, match=msg):
        temp_hdfstore.select_as_multiple(["df3"], where=["A>0", "B>0"], selector="df1")

    with pytest.raises(KeyError, match="'No object named df4 in the file'"):
        temp_hdfstore.select_as_multiple(
            ["df1", "df2"], where=["A>0", "B>0"], selector="df4"
        )

    # default select
    result = temp_hdfstore.select("df1", ["A>0", "B>0"])
    expected = temp_hdfstore.select_as_multiple(
        ["df1"], where=["A>0", "B>0"], selector="df1"
    )
    tm.assert_frame_equal(result, expected)
    expected = temp_hdfstore.select_as_multiple(
        "df1", where=["A>0", "B>0"], selector="df1"
    )
    tm.assert_frame_equal(result, expected)

    # multiple
    result = temp_hdfstore.select_as_multiple(
        ["df1", "df2"], where=["A>0", "B>0"], selector="df1"
    )
    expected = concat([df1, df2], axis=1)
    expected = expected[(expected.A > 0) & (expected.B > 0)]
    tm.assert_frame_equal(result, expected, check_freq=False)
    # FIXME: 2021-01-20 this is failing with freq None vs 4B on some builds

    # multiple (diff selector)
    result = temp_hdfstore.select_as_multiple(
        ["df1", "df2"], where="index>df2.index[4]", selector="df2"
    )
    expected = concat([df1, df2], axis=1)
    expected = expected[5:]
    tm.assert_frame_equal(result, expected)

    # test exception for diff rows
    df3 = df1.copy().head(2)
    temp_hdfstore.append("df3", df3)
    msg = "all tables must have exactly the same nrows!"
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.select_as_multiple(
            ["df1", "df3"], where=["A>0", "B>0"], selector="df1"
        )

