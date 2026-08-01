
def test_to_hdf_with_object_column_names_should_run(temp_h5_path, dtype):
    # GH9057
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 2)),
        columns=Index(["a", "b"], dtype=dtype),
    )
    df.to_hdf(temp_h5_path, key="df", format="table", data_columns=True)
    result = read_hdf(temp_h5_path, "df", where=f"index = [{df.index[0]}]")
    assert len(result)

