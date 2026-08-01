
def test_merge_empty_frames_column_order(left_empty, right_empty):
    # GH 51929
    df1 = DataFrame(1, index=[0], columns=["A", "B"])
    df2 = DataFrame(1, index=[0], columns=["A", "C", "D"])

    if left_empty:
        df1 = df1.iloc[:0]
    if right_empty:
        df2 = df2.iloc[:0]

    result = merge(df1, df2, on=["A"], how="outer")
    expected = DataFrame(1, index=range(1), columns=["A", "B", "C", "D"])
    if left_empty and right_empty:
        expected = expected.iloc[:0]
    elif left_empty:
        expected["B"] = np.nan
    elif right_empty:
        expected[["C", "D"]] = np.nan
    tm.assert_frame_equal(result, expected)

