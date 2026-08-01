
def test_series_index_name(df):
    grouped = df.loc[:, ["C"]].groupby(df["A"])
    result = grouped.agg(lambda x: x.mean())
    assert result.index.name == "A"

