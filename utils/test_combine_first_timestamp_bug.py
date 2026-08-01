
def test_combine_first_timestamp_bug(scalar1, scalar2, nulls_fixture):
    # GH28481
    na_value = nulls_fixture

    frame = DataFrame([[na_value, na_value]], columns=["a", "b"])
    other = DataFrame([[scalar1, scalar2]], columns=["b", "c"])

    common_dtype = find_common_type([frame.dtypes["b"], other.dtypes["b"]])

    if (
        is_dtype_equal(common_dtype, "object")
        or frame.dtypes["b"] == other.dtypes["b"]
        or frame.dtypes["b"].kind == frame.dtypes["b"].kind == "M"
    ):
        val = scalar1
    else:
        val = na_value

    result = frame.combine_first(other)

    expected = DataFrame([[na_value, val, scalar2]], columns=["a", "b", "c"])

    expected["b"] = expected["b"].astype(common_dtype)

    tm.assert_frame_equal(result, expected)

