
def test_store_mixed(compression, temp_h5_path):
    def _make_one():
        df = DataFrame(
            1.1 * np.arange(120).reshape((30, 4)),
            columns=Index(list("ABCD")),
            index=Index([f"i-{i}" for i in range(30)]),
        )
        df["obj1"] = "foo"
        df["obj2"] = "bar"
        df["bool1"] = df["A"] > 0
        df["bool2"] = df["B"] > 0
        df["int1"] = 1
        df["int2"] = 2
        return df._consolidate()

    df1 = _make_one()
    df2 = _make_one()

    _check_roundtrip(df1, tm.assert_frame_equal, path=temp_h5_path)
    _check_roundtrip(df2, tm.assert_frame_equal, path=temp_h5_path)

    with HDFStore(temp_h5_path) as store:
        store["obj"] = df1
        tm.assert_frame_equal(store["obj"], df1)
        store["obj"] = df2
        tm.assert_frame_equal(store["obj"], df2)

    # check that can store Series of all of these types
    _check_roundtrip(
        df1["obj1"],
        tm.assert_series_equal,
        path=temp_h5_path,
        compression=compression,
    )
    _check_roundtrip(
        df1["bool1"],
        tm.assert_series_equal,
        path=temp_h5_path,
        compression=compression,
    )
    _check_roundtrip(
        df1["int1"],
        tm.assert_series_equal,
        path=temp_h5_path,
        compression=compression,
    )

