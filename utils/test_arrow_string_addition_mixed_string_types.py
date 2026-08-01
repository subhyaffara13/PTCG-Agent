
def test_arrow_string_addition_mixed_string_types():
    # https://github.com/pandas-dev/pandas/issues/65220
    left = pd.Series(["a", None], dtype=ArrowDtype(pa.string()))
    right = pd.Series(["b", "c"], dtype=ArrowDtype(pa.large_string()))

    result = left + right
    expected = pd.Series(["ab", None], dtype=ArrowDtype(pa.large_string()))
    tm.assert_series_equal(result, expected)

    reflected_result = right + left
    expected_reflected = pd.Series(["ba", None], dtype=ArrowDtype(pa.large_string()))
    tm.assert_series_equal(reflected_result, expected_reflected)

