
def test_groupby_aggregation_func_list_multi_index_duplicate_columns():
    # GH#55041
    df = DataFrame(
        [
            [1, -9843, 43, 54, 7867],
            [2, 940, 9, -34, 44],
            [1, -34, 546, -549358, 0],
            [2, 244, -33, -100, 44],
        ],
        columns=MultiIndex(
            levels=[["level1.1", "level1.2"], ["level2.1", "level2.2"]],
            codes=[[0, 0, 0, 1, 1], [0, 1, 1, 0, 1]],
        ),
        index=MultiIndex(
            levels=[["level1.1", "level1.2"], ["level2.1", "level2.2"]],
            codes=[[0, 0, 0, 1], [0, 1, 1, 0]],
        ),
    )
    gb = df.groupby(level=0)
    result = gb.agg({("level1.1", "level2.2"): ["min", "max"]})

    expected = DataFrame(
        [[-9843, 940, 9, 546], [244, 244, -33, -33]],
        columns=MultiIndex(
            levels=[["level1.1"], ["level2.2"], ["min", "max"]],
            codes=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 1]],
        ),
        index=Index(["level1.1", "level1.2"]),
    )
    tm.assert_frame_equal(result, expected)

