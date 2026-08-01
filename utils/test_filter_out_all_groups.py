
def test_filter_out_all_groups():
    s = Series([1, 3, 20, 5, 22, 24, 7])
    grouper = s.apply(lambda x: x % 2)
    grouped = s.groupby(grouper)
    tm.assert_series_equal(grouped.filter(lambda x: x.mean() > 1000), s[[]])
    df = DataFrame({"A": [1, 12, 12, 1], "B": "a b c d".split()})
    grouper = df["A"].apply(lambda x: x % 2)
    grouped = df.groupby(grouper)
    tm.assert_frame_equal(grouped.filter(lambda x: x["A"].sum() > 1000), df.loc[[]])

