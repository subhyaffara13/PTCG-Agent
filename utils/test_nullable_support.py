
def test_nullable_support(dtype, version, temp_file):
    df = DataFrame(
        {
            "a": Series([1.0, 2.0, 3.0]),
            "b": Series([1, pd.NA, pd.NA], dtype=dtype.name),
            "c": Series(["a", "b", None]),
        }
    )
    dtype_name = df.b.dtype.numpy_dtype.name
    # Only use supported names: no uint, bool or int64
    dtype_name = dtype_name.replace("u", "")
    if dtype_name == "int64":
        dtype_name = "int32"
    elif dtype_name == "bool":
        dtype_name = "int8"
    value = StataMissingValue.BASE_MISSING_VALUES[dtype_name]
    smv = StataMissingValue(value)
    expected_b = Series([1, smv, smv], dtype=object, name="b")
    expected_c = Series(["a", "b", ""], name="c")
    df.to_stata(temp_file, write_index=False, version=version)
    reread = read_stata(temp_file, convert_missing=True)
    tm.assert_series_equal(df.a, reread.a)
    tm.assert_series_equal(reread.b, expected_b)
    tm.assert_series_equal(reread.c, expected_c)

