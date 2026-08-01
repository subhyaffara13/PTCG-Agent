
def test_keys_ignore_hdf_softlink(temp_hdfstore):
    # GH 20523
    # Puts a softlink into HDF file and rereads
    df = DataFrame({"A": range(5), "B": range(5)})
    temp_hdfstore.put("df", df)

    assert temp_hdfstore.keys() == ["/df"]

    temp_hdfstore._handle.create_soft_link(temp_hdfstore._handle.root, "symlink", "df")

    # Should ignore the softlink
    assert temp_hdfstore.keys() == ["/df"]

