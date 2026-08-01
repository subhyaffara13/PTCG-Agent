
def test_filter_with_non_values():
    # GH 62501
    df = DataFrame(
        [
            [1],
            [None],
        ],
        columns=["a"],
    )

    result = df.groupby("a", dropna=False).filter(lambda x: True)
    tm.assert_frame_equal(result, df)

