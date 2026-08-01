
def test_sum_mixed_empty(any_string_dtype):
    # GH 64657
    # for actual string dtype, sum gives "", for object dtype we get 0
    expected = Series(
        {"col1": "" if any_string_dtype == "string" else 0, "col2": 0}, dtype=object
    )
    empty_df = DataFrame(columns=["col1", "col2"]).astype(
        {"col1": any_string_dtype, "col2": int}
    )
    result = empty_df.sum()
    tm.assert_series_equal(result, expected)

