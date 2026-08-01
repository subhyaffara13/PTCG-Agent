
def test_groupby_agg_dict_with_getitem():
    # issue 25471
    dat = DataFrame({"A": ["A", "A", "B", "B", "B"], "B": [1, 2, 1, 1, 2]})
    result = dat.groupby("A")[["B"]].agg({"B": "sum"})

    expected = DataFrame({"B": [3, 4]}, index=["A", "B"]).rename_axis("A", axis=0)

    tm.assert_frame_equal(result, expected)

