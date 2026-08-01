
def test_groupby_transform_with_datetimes(func, values):
    # GH 15306
    dates = date_range("1/1/2011", periods=10, freq="D", unit="ns")

    stocks = DataFrame({"price": np.arange(10.0)}, index=dates)
    stocks["week_id"] = dates.isocalendar().week

    result = stocks.groupby(stocks["week_id"])["price"].transform(func)

    expected = Series(
        data=pd.to_datetime(values).as_unit("ns"), index=dates, name="price"
    )

    tm.assert_series_equal(result, expected)

