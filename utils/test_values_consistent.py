
def test_values_consistent(arr, expected_type, dtype, using_infer_string):
    if using_infer_string and dtype == "object":
        expected_type = ArrowStringArray if HAS_PYARROW else StringArray
    l_values = Series(arr)._values
    r_values = pd.Index(arr)._values
    assert type(l_values) is expected_type
    assert type(l_values) is type(r_values)

    tm.assert_equal(l_values, r_values)

