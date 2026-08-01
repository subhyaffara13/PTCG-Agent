
def test_stack_preserves_na(dtype, na_value, test_multiindex):
    # GH#56573
    if test_multiindex:
        index = MultiIndex.from_arrays(2 * [Index([na_value], dtype=dtype)])
    else:
        index = Index([na_value], dtype=dtype)
    df = DataFrame({"a": [1]}, index=index)
    result = df.stack()

    if test_multiindex:
        expected_index = MultiIndex.from_arrays(
            [
                Index([na_value], dtype=dtype),
                Index([na_value], dtype=dtype),
                Index(["a"]),
            ]
        )
    else:
        expected_index = MultiIndex.from_arrays(
            [
                Index([na_value], dtype=dtype),
                Index(["a"]),
            ]
        )
    expected = Series(1, index=expected_index)
    tm.assert_series_equal(result, expected)

