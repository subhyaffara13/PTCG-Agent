
def test_complibs_default_settings(temp_h5_path, using_infer_string):
    # GH15943
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )

    # Set complevel and check if complib is automatically set to
    # default value
    df.to_hdf(temp_h5_path, key="df", complevel=9)
    result = read_hdf(temp_h5_path, "df")
    expected = df.copy()
    if using_infer_string:
        expected.index = expected.index.astype("str")
        expected.columns = expected.columns.astype("str")
    tm.assert_frame_equal(result, expected)

    with tables.open_file(temp_h5_path, mode="r") as h5file:
        for node in h5file.walk_nodes(where="/df", classname="Leaf"):
            assert node.filters.complevel == 9
            assert node.filters.complib == "zlib"

    # Set complib and check to see if compression is disabled
    df.to_hdf(temp_h5_path, key="df", complib="zlib")
    result = read_hdf(temp_h5_path, "df")
    expected = df.copy()
    if using_infer_string:
        expected.index = expected.index.astype("str")
        expected.columns = expected.columns.astype("str")
    tm.assert_frame_equal(result, expected)

    with tables.open_file(temp_h5_path, mode="r") as h5file:
        for node in h5file.walk_nodes(where="/df", classname="Leaf"):
            assert node.filters.complevel == 0
            assert node.filters.complib is None

    # Check if not setting complib or complevel results in no compression
    df.to_hdf(temp_h5_path, key="df")
    result = read_hdf(temp_h5_path, "df")
    expected = df.copy()
    if using_infer_string:
        expected.index = expected.index.astype("str")
        expected.columns = expected.columns.astype("str")
    tm.assert_frame_equal(result, expected)

    with tables.open_file(temp_h5_path, mode="r") as h5file:
        for node in h5file.walk_nodes(where="/df", classname="Leaf"):
            assert node.filters.complevel == 0
            assert node.filters.complib is None

