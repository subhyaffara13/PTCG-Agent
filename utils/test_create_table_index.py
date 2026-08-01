
def test_create_table_index(temp_hdfstore):
    store = temp_hdfstore

    def col(t, column):
        return getattr(store.get_storer(t).table.cols, column)

    # data columns
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    df["string"] = "foo"
    df["string2"] = "bar"
    store.append("f", df, data_columns=["string", "string2"])
    assert col("f", "index").is_indexed is True
    assert col("f", "string").is_indexed is True
    assert col("f", "string2").is_indexed is True

    # specify index=columns
    store.append("f2", df, index=["string"], data_columns=["string", "string2"])
    assert col("f2", "index").is_indexed is False
    assert col("f2", "string").is_indexed is True
    assert col("f2", "string2").is_indexed is False

    # try to index a non-table
    store.put("f2", df)
    msg = "cannot create table index on a Fixed format store"
    with pytest.raises(TypeError, match=msg):
        store.create_table_index("f2")

