
def test_nunique_transform_with_datetime():
    # GH 35109 - transform with nunique on datetimes results in integers
    df = DataFrame(date_range("2008-12-31", "2009-01-02"), columns=["date"])
    result = df.groupby([0, 0, 1])["date"].transform("nunique")
    expected = Series([2, 2, 1], name="date")
    tm.assert_series_equal(result, expected)

