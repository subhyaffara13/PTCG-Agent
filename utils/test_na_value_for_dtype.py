
def test_na_value_for_dtype(dtype, na_value):
    result = na_value_for_dtype(pandas_dtype(dtype))
    # identify check doesn't work for datetime64/timedelta64("NaT") bc they
    #  are not singletons
    assert result is na_value or (
        isna(result) and isna(na_value) and type(result) is type(na_value)
    )

