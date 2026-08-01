
def test_groupby_agg_err_catching(err_cls):
    # make sure we suppress anything other than TypeError or AssertionError
    #  in _python_agg_general

    # Use a non-standard EA to make sure we don't go down ndarray paths
    from pandas.tests.extension.decimal.array import (
        DecimalArray,
        make_data,
        to_decimal,
    )

    data = make_data(5)
    df = DataFrame(
        {"id1": [0, 0, 0, 1, 1], "id2": [0, 1, 0, 1, 1], "decimals": DecimalArray(data)}
    )

    expected = Series(to_decimal([data[0], data[3]]))

    def weird_func(x):
        # weird function that raise something other than TypeError or IndexError
        #  in _python_agg_general
        if len(x) == 0:
            raise err_cls
        return x.iloc[0]

    result = df["decimals"].groupby(df["id1"]).agg(weird_func)
    tm.assert_series_equal(result, expected, check_names=False)

