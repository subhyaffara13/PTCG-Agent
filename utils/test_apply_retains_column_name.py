
def test_apply_retains_column_name(by_row):
    # GH 16380
    df = DataFrame({"x": range(3)}, Index(range(3), name="x"))
    result = df.x.apply(lambda x: Series(range(x + 1), Index(range(x + 1), name="y")))
    expected = DataFrame(
        [[0.0, np.nan, np.nan], [0.0, 1.0, np.nan], [0.0, 1.0, 2.0]],
        columns=Index(range(3), name="y"),
        index=Index(range(3), name="x"),
    )
    tm.assert_frame_equal(result, expected)

