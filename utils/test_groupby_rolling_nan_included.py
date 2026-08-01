
def test_groupby_rolling_nan_included():
    # GH 35542
    data = {"group": ["g1", np.nan, "g1", "g2", np.nan], "B": [0, 1, 2, 3, 4]}
    df = DataFrame(data)
    result = df.groupby("group", dropna=False).rolling(1, min_periods=1).mean()
    expected = DataFrame(
        {"B": [0.0, 2.0, 3.0, 1.0, 4.0]},
        # GH-38057 from_tuples puts the NaNs in the codes, result expects them
        # to be in the levels, at the moment
        # index=MultiIndex.from_tuples(
        #     [("g1", 0), ("g1", 2), ("g2", 3), (np.nan, 1), (np.nan, 4)],
        #     names=["group", None],
        # ),
        index=MultiIndex(
            [["g1", "g2", np.nan], [0, 1, 2, 3, 4]],
            [[0, 0, 1, 2, 2], [0, 2, 3, 1, 4]],
            names=["group", None],
        ),
    )
    tm.assert_frame_equal(result, expected)

