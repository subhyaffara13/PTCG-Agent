
def test_getitem_multiple():
    # GH 13174
    # multiple calls after selection causing an issue with aliasing
    data = [{"id": 1, "buyer": "A"}, {"id": 2, "buyer": "B"}]
    df = DataFrame(data, index=date_range("2016-01-01", periods=2))
    r = df.groupby("id").resample("1D")
    result = r["buyer"].count()

    exp_mi = pd.MultiIndex.from_arrays([[1, 2], df.index], names=("id", None))
    expected = Series(
        [1, 1],
        index=exp_mi,
        name="buyer",
    )
    tm.assert_series_equal(result, expected)

    result = r["buyer"].count()
    tm.assert_series_equal(result, expected)

