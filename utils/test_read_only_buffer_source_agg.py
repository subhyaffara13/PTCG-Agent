
def test_read_only_buffer_source_agg(agg):
    # https://github.com/pandas-dev/pandas/issues/36014
    df = DataFrame(
        {
            "sepal_length": [5.1, 4.9, 4.7, 4.6, 5.0],
            "species": ["setosa", "setosa", "setosa", "setosa", "setosa"],
        }
    )
    df._mgr.blocks[0].values.flags.writeable = False

    result = df.groupby(["species"]).agg({"sepal_length": agg})
    expected = df.copy().groupby(["species"]).agg({"sepal_length": agg})

    tm.assert_equal(result, expected)

