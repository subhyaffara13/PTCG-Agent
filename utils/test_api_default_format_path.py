
def test_api_default_format_path(temp_h5_path):
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )

    with pd.option_context("io.hdf.default_format", "fixed"):
        df.to_hdf(temp_h5_path, key="df")
        with HDFStore(temp_h5_path) as store:
            assert not store.get_storer("df").is_table
        msg = "Can only append to Tables"
        with pytest.raises(ValueError, match=msg):
            df.to_hdf(temp_h5_path, key="df2", append=True)

    with pd.option_context("io.hdf.default_format", "table"):
        df.to_hdf(temp_h5_path, key="df3")
        with HDFStore(temp_h5_path) as store:
            assert store.get_storer("df3").is_table
        df.to_hdf(temp_h5_path, key="df4", append=True)
        with HDFStore(temp_h5_path) as store:
            assert store.get_storer("df4").is_table

