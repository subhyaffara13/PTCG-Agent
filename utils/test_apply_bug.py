
def test_apply_bug():
    # GH 6125
    positions = DataFrame(
        [
            [1, "ABC0", 50],
            [1, "YUM0", 20],
            [1, "DEF0", 20],
            [2, "ABC1", 50],
            [2, "YUM1", 20],
            [2, "DEF1", 20],
        ],
        columns=["a", "market", "position"],
    )

    def f(r):
        return r["market"]

    expected = positions.apply(f, axis=1)

    positions = DataFrame(
        [
            [datetime(2013, 1, 1), "ABC0", 50],
            [datetime(2013, 1, 2), "YUM0", 20],
            [datetime(2013, 1, 3), "DEF0", 20],
            [datetime(2013, 1, 4), "ABC1", 50],
            [datetime(2013, 1, 5), "YUM1", 20],
            [datetime(2013, 1, 6), "DEF1", 20],
        ],
        columns=["a", "market", "position"],
    )
    result = positions.apply(f, axis=1)
    tm.assert_series_equal(result, expected)

