
def test_complex_series_error(temp_h5_path):
    complex128 = np.array([1.0 + 1.0j, 1.0 + 1.0j, 1.0 + 1.0j, 1.0 + 1.0j])
    s = Series(complex128, index=list("abcd"))

    msg = (
        "Columns containing complex values can be stored "
        "but cannot be indexed when using table format. "
        "Either use fixed format, set index=False, "
        "or do not include the columns containing complex "
        "values to data_columns when initializing the table."
    )

    with pytest.raises(TypeError, match=msg):
        s.to_hdf(temp_h5_path, key="obj", format="t")

    s.to_hdf(temp_h5_path, key="obj", format="t", index=False)
    reread = read_hdf(temp_h5_path, "obj")
    tm.assert_series_equal(s, reread)

