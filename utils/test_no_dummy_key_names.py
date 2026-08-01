
def test_no_dummy_key_names(df):
    # see gh-1291
    result = df.groupby(df["A"].values).sum()
    assert result.index.name is None

    result2 = df.groupby([df["A"].values, df["B"].values]).sum()
    assert result2.index.names == (None, None)

