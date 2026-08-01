
def test_type_comparison_with_real_numpy_dtype(any_real_numpy_dtype):
    # GH#43038
    assert pandas_dtype(any_real_numpy_dtype) == any_real_numpy_dtype

