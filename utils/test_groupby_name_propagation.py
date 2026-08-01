
def test_groupby_name_propagation(df):
    # GH 6124
    def summarize(df, name=None):
        return Series({"count": 1, "mean": 2, "omissions": 3}, name=name)

    def summarize_random_name(df):
        # Provide a different name for each Series.  In this case, groupby
        # should not attempt to propagate the Series name since they are
        # inconsistent.
        return Series({"count": 1, "mean": 2, "omissions": 3}, name=df.iloc[0]["C"])

    metrics = df.groupby("A").apply(summarize)
    assert metrics.columns.name is None
    metrics = df.groupby("A").apply(summarize, "metrics")
    assert metrics.columns.name == "metrics"
    metrics = df.groupby("A").apply(summarize_random_name)
    assert metrics.columns.name is None

