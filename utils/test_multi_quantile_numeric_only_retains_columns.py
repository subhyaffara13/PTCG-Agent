
def test_multi_quantile_numeric_only_retains_columns():
    df = DataFrame(list("abc"))
    result = df.quantile([0.5, 0.7], numeric_only=True)
    expected = DataFrame(index=[0.5, 0.7])
    tm.assert_frame_equal(
        result, expected, check_index_type=True, check_column_type=True
    )

