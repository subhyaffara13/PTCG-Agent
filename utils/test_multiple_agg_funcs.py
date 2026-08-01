
def test_multiple_agg_funcs(func, window_size, expected_vals):
    # GH 15072
    df = DataFrame(
        [
            ["A", 10, 20],
            ["A", 20, 30],
            ["A", 30, 40],
            ["B", 10, 30],
            ["B", 30, 40],
            ["B", 40, 80],
            ["B", 80, 90],
        ],
        columns=["stock", "low", "high"],
    )

    f = getattr(df.groupby("stock"), func)
    if window_size:
        window = f(window_size)
    else:
        window = f()

    index = MultiIndex.from_tuples(
        [("A", 0), ("A", 1), ("A", 2), ("B", 3), ("B", 4), ("B", 5), ("B", 6)],
        names=["stock", None],
    )
    columns = MultiIndex.from_tuples(
        [("low", "mean"), ("low", "max"), ("high", "mean"), ("high", "min")]
    )
    expected = DataFrame(expected_vals, index=index, columns=columns)

    result = window.agg({"low": ["mean", "max"], "high": ["mean", "min"]})

    tm.assert_frame_equal(result, expected)

