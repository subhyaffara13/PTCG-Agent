
def test_groupby_multi_index_codes():
    # GH#54347
    df = DataFrame(
        {"A": [1, 2, 3, 4], "B": [1, float("nan"), 2, float("nan")], "C": [2, 4, 6, 8]}
    )
    df_grouped = df.groupby(["A", "B"], dropna=False).sum()

    index = df_grouped.index
    tm.assert_index_equal(index, MultiIndex.from_frame(index.to_frame()))

