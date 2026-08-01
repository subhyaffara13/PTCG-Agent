
def test_pass_spec_to_storer(temp_hdfstore):
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )

    temp_hdfstore.put("df", df)
    msg = (
        "cannot pass a column specification when reading a Fixed format "
        "store. this store must be selected in its entirety"
    )
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.select("df", columns=["A"])
    msg = (
        "cannot pass a where specification when reading from a Fixed "
        "format store. this store must be selected in its entirety"
    )
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.select("df", where=["columns=A"])

