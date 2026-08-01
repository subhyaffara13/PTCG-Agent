
def test_apply_map_evaluate_lambdas_the_same(string_series, func, by_row, engine):
    # test that we are evaluating row-by-row first if by_row="compat"
    # else vectorized evaluation
    result = string_series.apply(func, by_row=by_row)

    if by_row:
        expected = string_series.map(func, engine=engine)
        tm.assert_series_equal(result, expected)
    else:
        assert result == str(string_series)

