
def test_duplicate_column_name(temp_h5_path):
    df = DataFrame(columns=["a", "a"], data=[[0, 0]])

    msg = "Columns index has to be unique for fixed format"
    with pytest.raises(ValueError, match=msg):
        df.to_hdf(temp_h5_path, key="df", format="fixed")

    df.to_hdf(temp_h5_path, key="df", format="table")
    other = read_hdf(temp_h5_path, "df")

    tm.assert_frame_equal(df, other)
    assert df.equals(other)
    assert other.equals(df)

