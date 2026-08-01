
def test_complex_across_dimensions(temp_h5_path):
    complex128 = np.array([1.0 + 1.0j, 1.0 + 1.0j, 1.0 + 1.0j, 1.0 + 1.0j])
    s = Series(complex128, index=list("abcd"))
    df = DataFrame({"A": s, "B": s})

    df.to_hdf(temp_h5_path, key="obj", format="table")
    reread = read_hdf(temp_h5_path, "obj")
    tm.assert_frame_equal(df, reread)

