
def test_agg_evaluate_lambdas(string_series):
    # GH53325
    result = string_series.agg(lambda x: type(x))
    assert result is Series

    result = string_series.agg(type)
    assert result is Series

