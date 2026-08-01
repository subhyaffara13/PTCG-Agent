
def test_resample_apply_with_additional_args(unit):
    # GH 14615
    index = date_range("1/1/2000 00:00:00", "1/1/2000 00:13:00", freq="Min")
    series = Series(range(len(index)), index=index)
    series.index.name = "index"

    def f(data, add_arg):
        return np.mean(data) * add_arg

    series.index = series.index.as_unit(unit)

    multiplier = 10
    result = series.resample("D").apply(f, multiplier)
    expected = series.resample("D").mean().multiply(multiplier)
    tm.assert_series_equal(result, expected)

    # Testing as kwarg
    result = series.resample("D").apply(f, add_arg=multiplier)
    expected = series.resample("D").mean().multiply(multiplier)
    tm.assert_series_equal(result, expected)

