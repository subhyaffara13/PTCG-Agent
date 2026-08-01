
def test_groupby_as_index_select_column_sum_empty_df():
    # GH 35246
    df = DataFrame(columns=Index(["A", "B", "C"], name="alpha"))
    left = df.groupby(by="A", as_index=False)["B"].sum(numeric_only=False)

    expected = DataFrame(columns=df.columns[:2], index=range(0))
    # GH#50744 - Columns after selection shouldn't retain names
    expected.columns.names = [None]
    tm.assert_frame_equal(left, expected)

