
def test_round_trip_equals(temp_h5_path):
    # GH 9330
    df = DataFrame({"B": [1, 2], "A": ["x", "y"]})

    df.to_hdf(temp_h5_path, key="df", format="table")
    other = read_hdf(temp_h5_path, "df")
    tm.assert_frame_equal(df, other)
    assert df.equals(other)
    assert other.equals(df)

