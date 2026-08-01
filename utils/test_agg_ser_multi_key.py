
def test_agg_ser_multi_key(df):
    f = lambda x: x.sum()
    results = df.C.groupby([df.A, df.B]).aggregate(f)
    expected = df.groupby(["A", "B"]).sum()["C"]
    tm.assert_series_equal(results, expected)

