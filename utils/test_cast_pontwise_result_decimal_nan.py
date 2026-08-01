
def test_cast_pontwise_result_decimal_nan():
    # GH#62522 we don't want to get back null[pyarrow] here
    ser = pd.Series([], dtype="float64[pyarrow]")
    arr = ser.array
    item = Decimal("NaN")

    result = arr._cast_pointwise_result([item])

    pa_type = result.dtype.pyarrow_dtype
    assert pa.types.is_decimal(pa_type)

