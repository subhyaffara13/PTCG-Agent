
def test_filter_multi_column_df():
    df = DataFrame({"A": [1, 12, 12, 1], "B": [1, 1, 1, 1]})
    grouper = df["A"].apply(lambda x: x % 2)
    grouped = df.groupby(grouper)
    expected = DataFrame({"A": [12, 12], "B": [1, 1]}, index=[1, 2])
    tm.assert_frame_equal(
        grouped.filter(lambda x: x["A"].sum() - x["B"].sum() > 10), expected
    )

