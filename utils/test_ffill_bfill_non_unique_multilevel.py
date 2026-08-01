
def test_ffill_bfill_non_unique_multilevel(func, expected_status):
    # GH 19437
    date = pd.to_datetime(
        [
            "2018-01-01",
            "2018-01-01",
            "2018-01-01",
            "2018-01-01",
            "2018-01-02",
            "2018-01-01",
            "2018-01-02",
        ]
    )
    symbol = ["MSFT", "MSFT", "MSFT", "AAPL", "AAPL", "TSLA", "TSLA"]
    status = ["shrt", np.nan, "lng", np.nan, "shrt", "ntrl", np.nan]

    df = DataFrame({"date": date, "symbol": symbol, "status": status})
    df = df.set_index(["date", "symbol"])
    result = getattr(df.groupby("symbol")["status"], func)()

    index = MultiIndex.from_tuples(
        tuples=list(zip(*[date, symbol], strict=True)), names=["date", "symbol"]
    )
    expected = Series(expected_status, index=index, name="status")

    tm.assert_series_equal(result, expected)

