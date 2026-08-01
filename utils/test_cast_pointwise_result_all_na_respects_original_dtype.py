
def test_cast_pointwise_result_all_na_respects_original_dtype(arr):
    # GH#62344
    values = [pd.NA, pd.NA]
    result = arr._cast_pointwise_result(values)
    assert result.dtype == arr.dtype
    assert all(x is pd.NA for x in result)

