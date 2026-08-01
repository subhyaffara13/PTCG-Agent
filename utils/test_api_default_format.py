
def test_api_default_format(temp_hdfstore):
    # default_format option
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )

    with pd.option_context("io.hdf.default_format", "fixed"):
        temp_hdfstore.put("df", df)
        assert not temp_hdfstore.get_storer("df").is_table

        msg = "Can only append to Tables"
        with pytest.raises(ValueError, match=msg):
            temp_hdfstore.append("df2", df)

    with pd.option_context("io.hdf.default_format", "table"):
        temp_hdfstore.remove("df")
        temp_hdfstore.put("df", df)
        assert temp_hdfstore.get_storer("df").is_table

        temp_hdfstore.append("df2", df)
        assert temp_hdfstore.get_storer("df").is_table

