
def expected_dtype(dtype, method, pct=False):
    exp_dtype = "float64"
    # elif dtype in ["Int64", "Float64", "string[pyarrow]", "string[python]"]:
    if dtype in ["string[pyarrow]"]:
        exp_dtype = "Float64"
    elif dtype in ["float64[pyarrow]", "int64[pyarrow]"]:
        if method == "average" or pct:
            exp_dtype = "double[pyarrow]"
        else:
            exp_dtype = "uint64[pyarrow]"
    elif dtype in ["Float64", "Int64"]:
        if method == "average" or pct:
            exp_dtype = "Float64"
        else:
            exp_dtype = "UInt64"

    return exp_dtype

