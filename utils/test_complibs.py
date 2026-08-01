
def test_complibs(tmp_path, lvl, lib, request):
    # GH14478
    if is_platform_linux() and lib == "blosc2" and lvl != 0:
        request.applymarker(pytest.mark.xfail(reason=f"Fails for {lib} on Linux"))
    df = DataFrame(
        np.ones((30, 4)), columns=list("ABCD"), index=np.arange(30).astype(np.str_)
    )

    # Remove lzo if its not available on this platform
    if not tables.which_lib_version("lzo"):
        pytest.skip("lzo not available")
    # Remove bzip2 if its not available on this platform
    if not tables.which_lib_version("bzip2"):
        pytest.skip("bzip2 not available")

    tmpfile = tmp_path / f"{lvl}_{lib}.h5"
    gname = f"{lvl}_{lib}"

    # Write and read file to see if data is consistent
    df.to_hdf(tmpfile, key=gname, complib=lib, complevel=lvl)
    result = read_hdf(tmpfile, gname)
    tm.assert_frame_equal(result, df)

    is_mac = is_platform_mac()

    # Open file and check metadata for correct amount of compression
    with tables.open_file(tmpfile, mode="r") as h5table:
        for node in h5table.walk_nodes(where="/" + gname, classname="Leaf"):
            assert node.filters.complevel == lvl
            if lvl == 0:
                assert node.filters.complib is None
            elif is_mac and lib == "blosc2":
                res = node.filters.complib
                assert res in [lib, "blosc2:blosclz"], res
            else:
                assert node.filters.complib == lib

