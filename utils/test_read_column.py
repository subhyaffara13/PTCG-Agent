import re

def test_read_column(temp_hdfstore):
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )

    # GH 17912
    # HDFStore.select_column should raise a KeyError
    # exception if the key is not a valid store
    with pytest.raises(KeyError, match="No object named df in the file"):
        temp_hdfstore.select_column("df", "index")

    temp_hdfstore.append("df", df)
    # error
    with pytest.raises(
        KeyError, match=re.escape("'column [foo] not found in the table'")
    ):
        temp_hdfstore.select_column("df", "foo")

    msg = re.escape("select_column() got an unexpected keyword argument 'where'")
    with pytest.raises(TypeError, match=msg):
        temp_hdfstore.select_column("df", "index", where=["index>5"])

    # valid
    result = temp_hdfstore.select_column("df", "index")
    tm.assert_almost_equal(result.values, Series(df.index).values)
    assert isinstance(result, Series)

    # not a data indexable column
    msg = re.escape(
        "column [values_block_0] can not be extracted individually; "
        "it is not data indexable"
    )
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.select_column("df", "values_block_0")

    # a data column
    df2 = df.copy()
    df2["string"] = "foo"
    temp_hdfstore.append("df2", df2, data_columns=["string"])
    result = temp_hdfstore.select_column("df2", "string")
    tm.assert_almost_equal(result.values, df2["string"].values)

    # a data column with NaNs, result excludes the NaNs
    df3 = df.copy()
    df3["string"] = "foo"
    df3.loc[df3.index[4:6], "string"] = np.nan
    temp_hdfstore.append("df3", df3, data_columns=["string"])
    result = temp_hdfstore.select_column("df3", "string")
    tm.assert_almost_equal(result.values, df3["string"].values)

    # start/stop
    result = temp_hdfstore.select_column("df3", "string", start=2)
    tm.assert_almost_equal(result.values, df3["string"].values[2:])

    result = temp_hdfstore.select_column("df3", "string", start=-2)
    tm.assert_almost_equal(result.values, df3["string"].values[-2:])

    result = temp_hdfstore.select_column("df3", "string", stop=2)
    tm.assert_almost_equal(result.values, df3["string"].values[:2])

    result = temp_hdfstore.select_column("df3", "string", stop=-2)
    tm.assert_almost_equal(result.values, df3["string"].values[:-2])

    result = temp_hdfstore.select_column("df3", "string", start=2, stop=-2)
    tm.assert_almost_equal(result.values, df3["string"].values[2:-2])

    result = temp_hdfstore.select_column("df3", "string", start=-2, stop=2)
    tm.assert_almost_equal(result.values, df3["string"].values[-2:2])

    # GH 10392 - make sure column name is preserved
    df4 = DataFrame({"A": np.random.default_rng(2).standard_normal(10), "B": "foo"})
    temp_hdfstore.append("df4", df4, data_columns=True)
    expected = df4["B"]
    result = temp_hdfstore.select_column("df4", "B")
    tm.assert_series_equal(result, expected)

