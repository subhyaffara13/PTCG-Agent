
def test_astype_from_masked_float_with_nan(dtype, using_nan_is_na):
    # GH#61617, GH#65227 - FloatingArray.astype(str) with unmasked NaN
    arr = pd.array([np.nan, pd.NA, 3.0], dtype="Float64")
    result = arr.astype(dtype)
    if using_nan_is_na:
        expected = pd.array([pd.NA, pd.NA, "3.0"], dtype=dtype)
    else:
        expected = pd.array(["nan", pd.NA, "3.0"], dtype=dtype)
    tm.assert_extension_array_equal(result, expected)

