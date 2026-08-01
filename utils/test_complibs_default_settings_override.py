
def test_complibs_default_settings_override(temp_h5_path):
    # Check if file-defaults can be overridden on a per table basis
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )
    store = HDFStore(temp_h5_path)
    store.append("dfc", df, complevel=9, complib="blosc")
    store.append("df", df)
    store.close()

    with tables.open_file(temp_h5_path, mode="r") as h5file:
        for node in h5file.walk_nodes(where="/df", classname="Leaf"):
            assert node.filters.complevel == 0
            assert node.filters.complib is None
        for node in h5file.walk_nodes(where="/dfc", classname="Leaf"):
            assert node.filters.complevel == 9
            assert node.filters.complib == "blosc"

