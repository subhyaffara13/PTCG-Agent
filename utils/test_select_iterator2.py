
def test_select_iterator2(temp_h5_path):
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )
    df.to_hdf(temp_h5_path, key="df_non_table")

    msg = "can only use an iterator or chunksize on a table"
    with pytest.raises(TypeError, match=msg):
        read_hdf(temp_h5_path, "df_non_table", chunksize=2)

    with pytest.raises(TypeError, match=msg):
        read_hdf(temp_h5_path, "df_non_table", iterator=True)

