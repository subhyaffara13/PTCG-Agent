
def test_how_lambda_functions(simple_date_range_series, unit):
    ts = simple_date_range_series("1/1/2000", "4/1/2000")
    ts.index = ts.index.as_unit(unit)

    result = ts.resample("ME").apply(lambda x: x.mean())
    exp = ts.resample("ME").mean()
    tm.assert_series_equal(result, exp)

    foo_exp = ts.resample("ME").mean()
    foo_exp.name = "foo"
    bar_exp = ts.resample("ME").std()
    bar_exp.name = "bar"

    result = ts.resample("ME").apply([lambda x: x.mean(), lambda x: x.std(ddof=1)])
    result.columns = ["foo", "bar"]
    tm.assert_series_equal(result["foo"], foo_exp)
    tm.assert_series_equal(result["bar"], bar_exp)

    # this is a MI Series, so comparing the names of the results
    # doesn't make sense
    result = ts.resample("ME").aggregate(
        {"foo": lambda x: x.mean(), "bar": lambda x: x.std(ddof=1)}
    )
    tm.assert_series_equal(result["foo"], foo_exp, check_names=False)
    tm.assert_series_equal(result["bar"], bar_exp, check_names=False)

