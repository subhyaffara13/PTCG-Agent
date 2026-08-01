
def test_agg_must_agg(df):
    grouped = df.groupby("A")["C"]

    msg = "Must produce aggregated value"
    with pytest.raises(Exception, match=msg):
        grouped.agg(lambda x: x.describe())
    with pytest.raises(Exception, match=msg):
        grouped.agg(lambda x: x.index[:2])

