
def test_to_hdf_with_object_column_names_should_fail(temp_h5_path, columns):
    # GH9057
    df = DataFrame(np.random.default_rng(2).standard_normal((10, 2)), columns=columns)
    msg = "cannot have non-object label DataIndexableCol"
    with pytest.raises(ValueError, match=msg):
        df.to_hdf(temp_h5_path, key="df", format="table", data_columns=True)

