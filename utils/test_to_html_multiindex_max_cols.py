
def test_to_html_multiindex_max_cols(datapath):
    # GH 6131
    index = MultiIndex(
        levels=[["ba", "bb", "bc"], ["ca", "cb", "cc"]],
        codes=[[0, 1, 2], [0, 1, 2]],
        names=["b", "c"],
    )
    columns = MultiIndex(
        levels=[["d"], ["aa", "ab", "ac"]],
        codes=[[0, 0, 0], [0, 1, 2]],
        names=[None, "a"],
    )
    data = np.array(
        [[1.0, np.nan, np.nan], [np.nan, 2.0, np.nan], [np.nan, np.nan, 3.0]]
    )
    df = DataFrame(data, index, columns)
    result = df.to_html(max_cols=2)
    expected = expected_html(datapath, "gh6131_expected_output")
    assert result == expected

