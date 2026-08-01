
def test_with_string_args(datetime_series, all_numeric_reductions):
    result = datetime_series.apply(all_numeric_reductions)
    expected = getattr(datetime_series, all_numeric_reductions)()
    assert result == expected

