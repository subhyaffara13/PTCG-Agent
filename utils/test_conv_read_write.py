
def test_conv_read_write(temp_h5_path):
    def roundtrip(key, obj, **kwargs):
        obj.to_hdf(temp_h5_path, key=key, **kwargs)
        return read_hdf(temp_h5_path, key)

    o = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    tm.assert_series_equal(o, roundtrip("series", o))

    o = Series(range(10), dtype="float64", index=[f"i_{i}" for i in range(10)])
    tm.assert_series_equal(o, roundtrip("string_series", o))

    o = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )
    tm.assert_frame_equal(o, roundtrip("frame", o))

    # table
    df = DataFrame({"A": range(5), "B": range(5)})
    df.to_hdf(temp_h5_path, key="table", append=True)
    result = read_hdf(temp_h5_path, "table", where=["index>2"])
    tm.assert_frame_equal(df[df.index > 2], result)

