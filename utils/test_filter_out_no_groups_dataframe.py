
def test_filter_out_no_groups_dataframe():
    df = DataFrame({"A": [1, 12, 12, 1], "B": "a b c d".split()})
    grouper = df["A"].apply(lambda x: x % 2)
    grouped = df.groupby(grouper)
    filtered = grouped.filter(lambda x: x["A"].mean() > 0)
    tm.assert_frame_equal(filtered, df)

