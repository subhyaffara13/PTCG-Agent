
def test_to_html_multiindex_sparsify(multi_sparse, expected, datapath):
    index = MultiIndex.from_arrays([[0, 0, 1, 1], [0, 1, 0, 1]], names=["foo", None])
    df = DataFrame([[0, 1], [2, 3], [4, 5], [6, 7]], index=index)
    if expected.endswith("2"):
        df.columns = index[::2]
    with option_context("display.multi_sparse", multi_sparse):
        result = df.to_html()
    expected = expected_html(datapath, expected)
    assert result == expected

