
def test_to_html_multiindex_odd_even_truncate(max_rows, expected, datapath):
    # GH 14882 - Issue on truncation with odd length DataFrame
    index = MultiIndex.from_product(
        [[100, 200, 300], [10, 20, 30], [1, 2, 3, 4, 5, 6, 7]], names=["a", "b", "c"]
    )
    df = DataFrame({"n": range(len(index))}, index=index)
    result = df.to_html(max_rows=max_rows)
    expected = expected_html(datapath, expected)
    assert result == expected

