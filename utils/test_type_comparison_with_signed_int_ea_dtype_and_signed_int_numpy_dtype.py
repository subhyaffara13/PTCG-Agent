
def test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype(
    any_signed_int_ea_dtype, any_signed_int_numpy_dtype
):
    # GH#43038
    assert not pandas_dtype(any_signed_int_ea_dtype) == any_signed_int_numpy_dtype

