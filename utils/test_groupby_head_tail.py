
def test_groupby_head_tail(op, n, expected_rows, columns, as_index):
    df = DataFrame([[1, 2], [1, 4], [5, 6]], columns=["A", "B"])
    g = df.groupby("A", as_index=as_index)
    expected = df.iloc[expected_rows]
    if columns is not None:
        g = g[columns]
        expected = expected[columns]
    result = getattr(g, op)(n)
    tm.assert_frame_equal(result, expected)

