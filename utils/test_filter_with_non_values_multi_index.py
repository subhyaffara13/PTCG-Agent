
def test_filter_with_non_values_multi_index():
    # GH 62501
    df = DataFrame(
        [
            [1, 2],
            [3, None],
            [None, 4],
            [None, None],
        ],
        columns=["a", "b"],
    )

    result = df.groupby(["a", "b"], dropna=False).filter(lambda x: True)
    tm.assert_frame_equal(result, df)

