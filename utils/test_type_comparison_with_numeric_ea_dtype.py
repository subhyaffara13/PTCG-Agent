
def test_type_comparison_with_numeric_ea_dtype(any_numeric_ea_dtype):
    # GH#43038
    assert pandas_dtype(any_numeric_ea_dtype) == any_numeric_ea_dtype

