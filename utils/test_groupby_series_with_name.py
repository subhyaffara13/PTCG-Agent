
def test_groupby_series_with_name(df):
    result = df.groupby(df["A"]).mean(numeric_only=True)
    result2 = df.groupby(df["A"], as_index=False).mean(numeric_only=True)
    assert result.index.name == "A"
    assert "A" in result2

    result = df.groupby([df["A"], df["B"]]).mean()
    result2 = df.groupby([df["A"], df["B"]], as_index=False).mean()
    assert result.index.names == ("A", "B")
    assert "A" in result2
    assert "B" in result2

