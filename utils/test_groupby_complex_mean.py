
def test_groupby_complex_mean():
    # GH 26475
    df = DataFrame(
        [
            {"a": 2, "b": 1 + 2j},
            {"a": 1, "b": 1 + 1j},
            {"a": 1, "b": 1 + 2j},
        ]
    )
    result = df.groupby("b").mean()
    expected = DataFrame(
        [[1.0], [1.5]],
        index=Index([(1 + 1j), (1 + 2j)], name="b"),
        columns=Index(["a"]),
    )
    tm.assert_frame_equal(result, expected)

