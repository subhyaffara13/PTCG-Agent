
def test_groupby_resample_with_list_of_keys():
    # GH 47362
    df = DataFrame(
        data={
            "date": date_range(start="2016-01-01", periods=8),
            "group": [0, 0, 0, 0, 1, 1, 1, 1],
            "val": [1, 7, 5, 2, 3, 10, 5, 1],
        }
    )
    result = df.groupby("group").resample("2D", on="date")[["val"]].mean()

    mi_exp = pd.MultiIndex.from_arrays(
        [[0, 0, 1, 1], df["date"]._values[::2]], names=["group", "date"]
    )
    expected = DataFrame(
        data={
            "val": [4.0, 3.5, 6.5, 3.0],
        },
        index=mi_exp,
    )
    tm.assert_frame_equal(result, expected)

