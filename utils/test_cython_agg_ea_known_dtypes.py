
def test_cython_agg_EA_known_dtypes(data, op_name, action, with_na):
    if with_na:
        data[3] = pd.NA

    df = DataFrame({"key": ["a", "a", "b", "b"], "col": data})
    grouped = df.groupby("key")

    if action == "always_int":
        # always Int64
        expected_dtype = pd.Int64Dtype()
    elif action == "large_int":
        # for any int/bool use Int64, for float preserve dtype
        if is_float_dtype(data.dtype):
            expected_dtype = data.dtype
        elif is_integer_dtype(data.dtype):
            # match the numpy dtype we'd get with the non-nullable analogue
            expected_dtype = data.dtype
        else:
            expected_dtype = pd.Int64Dtype()
    elif action == "always_float":
        # for any int/bool use Float64, for float preserve dtype
        if is_float_dtype(data.dtype):
            expected_dtype = data.dtype
        else:
            expected_dtype = pd.Float64Dtype()
    elif action == "preserve":
        expected_dtype = data.dtype

    result = getattr(grouped, op_name)()
    assert result["col"].dtype == expected_dtype

    result = grouped.aggregate(op_name)
    assert result["col"].dtype == expected_dtype

    result = getattr(grouped["col"], op_name)()
    assert result.dtype == expected_dtype

    result = grouped["col"].aggregate(op_name)
    assert result.dtype == expected_dtype

