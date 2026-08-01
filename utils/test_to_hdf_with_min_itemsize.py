
def test_to_hdf_with_min_itemsize(temp_h5_path):
    # min_itemsize in index with to_hdf (GH 10381)
    df = DataFrame(
        {
            "A": [0.0, 1.0, 2.0, 3.0, 4.0],
            "B": [0.0, 1.0, 0.0, 1.0, 0.0],
            "C": Index(["foo1", "foo2", "foo3", "foo4", "foo5"]),
            "D": date_range("20130101", periods=5),
        }
    ).set_index("C")
    df.to_hdf(temp_h5_path, key="ss3", format="table", min_itemsize={"index": 6})
    # just make sure there is a longer string:
    df2 = df.copy().reset_index().assign(C="longer").set_index("C")
    df2.to_hdf(temp_h5_path, key="ss3", append=True, format="table")
    tm.assert_frame_equal(read_hdf(temp_h5_path, "ss3"), concat([df, df2]))

    # same as above, with a Series
    df["B"].to_hdf(temp_h5_path, key="ss4", format="table", min_itemsize={"index": 6})
    df2["B"].to_hdf(temp_h5_path, key="ss4", append=True, format="table")
    tm.assert_series_equal(read_hdf(temp_h5_path, "ss4"), concat([df["B"], df2["B"]]))

