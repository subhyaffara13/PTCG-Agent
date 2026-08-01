
def test_transform_bug():
    # GH 5712
    # transforming on a datetime column
    df = DataFrame({"A": Timestamp("20130101"), "B": np.arange(5)})
    result = df.groupby("A")["B"].transform(lambda x: x.rank(ascending=False))
    expected = Series(np.arange(5, 0, step=-1), name="B", dtype="float64")
    tm.assert_series_equal(result, expected)

