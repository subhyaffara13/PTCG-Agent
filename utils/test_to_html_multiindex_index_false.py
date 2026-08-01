
def test_to_html_multiindex_index_false(index_is_named, datapath):
    # GH 8452
    df = DataFrame(
        {"a": range(2), "b": range(3, 5), "c": range(5, 7), "d": range(3, 5)}
    )
    df.columns = MultiIndex.from_product([["a", "b"], ["c", "d"]])
    if index_is_named:
        df.index = Index(df.index.values, name="idx")
    result = df.to_html(index=False)
    expected = expected_html(datapath, "gh8452_expected_output")
    assert result == expected

