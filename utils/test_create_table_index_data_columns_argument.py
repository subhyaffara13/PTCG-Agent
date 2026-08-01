
def test_create_table_index_data_columns_argument(temp_hdfstore):
    # GH 28156

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
    store.append("f", df, data_columns=["string"])
    assert col("f", "index").is_indexed is True
    assert col("f", "string").is_indexed is True

    msg = "'Cols' object has no attribute 'string2'"
    with pytest.raises(AttributeError, match=msg):
        col("f", "string2").is_indexed

    # try to index a col which isn't a data_column
    msg = (
        "column string2 is not a data_column.\n"
        "In order to read column string2 you must reload the dataframe \n"
        "into HDFStore and include string2 with the data_columns argument."
    )
    with pytest.raises(AttributeError, match=msg):
        store.create_table_index("f", columns=["string2"])

