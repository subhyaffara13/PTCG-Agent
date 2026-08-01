
def test_coordinates_multiple_tables(temp_hdfstore):
    store = temp_hdfstore
    df1 = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    df2 = df1.copy().rename(columns="{}_2".format)
    store.append("df1", df1, data_columns=["A", "B"])
    store.append("df2", df2)

    c = store.select_as_coordinates("df1", ["A>0", "B>0"])
    df1_result = store.select("df1", c)
    df2_result = store.select("df2", c)
    result = concat([df1_result, df2_result], axis=1)

    expected = concat([df1, df2], axis=1)
    expected = expected[(expected.A > 0) & (expected.B > 0)]
    tm.assert_frame_equal(result, expected, check_freq=False)

