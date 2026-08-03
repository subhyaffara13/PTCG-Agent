import re

def test_table_values_dtypes_roundtrip(temp_hdfstore, using_infer_string):
    df1 = DataFrame({"a": [1, 2, 3]}, dtype="f8")
    temp_hdfstore.append("df_f8", df1)
    tm.assert_series_equal(df1.dtypes, temp_hdfstore["df_f8"].dtypes)

    df2 = DataFrame({"a": [1, 2, 3]}, dtype="i8")
    temp_hdfstore.append("df_i8", df2)
    tm.assert_series_equal(df2.dtypes, temp_hdfstore["df_i8"].dtypes)

    # incompatible dtype
    msg = re.escape(
        "Cannot serialize the column [a] "
        "because its data contents are not [float] "
        "but [integer] object dtype"
    )
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append("df_i8", df1)

    # check creation/storage/retrieval of float32 (a bit hacky to
    # actually create them thought)
    df1 = DataFrame(np.array([[1], [2], [3]], dtype="f4"), columns=["A"])
    temp_hdfstore.append("df_f4", df1)
    tm.assert_series_equal(df1.dtypes, temp_hdfstore["df_f4"].dtypes)
    assert df1.dtypes.iloc[0] == "float32"

    # check with mixed dtypes
    df1 = DataFrame(
        {
            c: Series(np.random.default_rng(2).integers(5), dtype=c)
            for c in ["float32", "float64", "int32", "int64", "int16", "int8"]
        }
    )
    df1["string"] = "foo"
    df1["float322"] = 1.0
    df1["float322"] = df1["float322"].astype("float32")
    df1["bool"] = df1["float32"] > 0
    df1["time_s_1"] = Timestamp("20130101").as_unit("s")
    df1["time_s_2"] = Timestamp("20130101 00:00:00").as_unit("s")
    df1["time_ms"] = Timestamp("20130101 00:00:00.000").as_unit("ms")
    df1["time_ns"] = Timestamp("20130102 00:00:00.000000000")

    temp_hdfstore.append("df_mixed_dtypes1", df1)
    result = temp_hdfstore.select("df_mixed_dtypes1").dtypes.value_counts()
    result.index = [str(i) for i in result.index]
    str_dtype = "str" if using_infer_string else "object"
    expected = Series(
        {
            "float32": 2,
            "float64": 1,
            "int32": 1,
            "bool": 1,
            "int16": 1,
            "int8": 1,
            "int64": 1,
            str_dtype: 1,
            "datetime64[s]": 2,
            "datetime64[ms]": 1,
            "datetime64[ns]": 1,
        },
        name="count",
    )
    result = result.sort_index()
    expected = expected.sort_index()
    tm.assert_series_equal(result, expected)

