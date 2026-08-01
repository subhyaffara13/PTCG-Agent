
def test_seriesgroupby_name_attr(df):
    # GH 6265
    result = df.groupby("A")["C"]
    assert result.count().name == "C"
    assert result.mean().name == "C"

    testFunc = lambda x: np.sum(x) * 2
    assert result.agg(testFunc).name == "C"

