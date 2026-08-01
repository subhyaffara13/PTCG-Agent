
def test_complex_across_dimensions_fixed(temp_h5_path):
    complex128 = np.array([1.0 + 1.0j, 1.0 + 1.0j, 1.0 + 1.0j, 1.0 + 1.0j])
    s = Series(complex128, index=list("abcd"))
    df = DataFrame({"A": s, "B": s})

    objs = [s, df]
    comps = [tm.assert_series_equal, tm.assert_frame_equal]
    for obj, comp in zip(objs, comps):
        obj.to_hdf(temp_h5_path, key="obj", format="fixed")
        reread = read_hdf(temp_h5_path, "obj")
        comp(obj, reread)

