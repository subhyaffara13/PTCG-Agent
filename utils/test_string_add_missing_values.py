
def test_string_add_missing_values(string_dtype_no_object):
    # GH#64968 Arrow-backed str arrays should return NA when added to missing
    arr = pd.array(["y"], dtype=string_dtype_no_object)
    expected = pd.array([NA], dtype=string_dtype_no_object)

    for na_val in [None, np.nan, NA]:
        # left side
        result = arr + na_val
        tm.assert_extension_array_equal(result, expected)

        # right side
        result = na_val + arr
        tm.assert_extension_array_equal(result, expected)

