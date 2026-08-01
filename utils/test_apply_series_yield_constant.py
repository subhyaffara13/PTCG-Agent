
def test_apply_series_yield_constant(df):
    result = df.groupby(["A", "B"])["C"].apply(len)
    assert result.index.names[:2] == ("A", "B")

