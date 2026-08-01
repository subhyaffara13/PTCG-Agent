
def test_groupby_resample_on_api_with_getitem():
    # GH 17813
    df = DataFrame(
        {"id": list("aabbb"), "date": date_range("1-1-2016", periods=5), "data": 1}
    )
    exp = df.set_index("date").groupby("id").resample("2D")["data"].sum()
    result = df.groupby("id").resample("2D", on="date")["data"].sum()
    tm.assert_series_equal(result, exp)

