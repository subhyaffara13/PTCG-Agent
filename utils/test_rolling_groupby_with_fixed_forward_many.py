
def test_rolling_groupby_with_fixed_forward_many(group_keys, window_size):
    # GH 43267
    df = DataFrame(
        {
            "a": np.array(list(group_keys)),
            "b": np.arange(len(group_keys), dtype=np.float64) + 17,
            "c": np.arange(len(group_keys), dtype=np.int64),
        }
    )

    indexer = FixedForwardWindowIndexer(window_size=window_size)
    result = df.groupby("a")["b"].rolling(window=indexer, min_periods=1).sum()
    result.index.names = ["a", "c"]

    groups = df.groupby("a")[["a", "b", "c"]]
    manual = concat(
        [
            g.assign(
                b=[
                    g["b"].iloc[i : i + window_size].sum(min_count=1)
                    for i in range(len(g))
                ]
            )
            for _, g in groups
        ]
    )
    manual = manual.set_index(["a", "c"])["b"]

    tm.assert_series_equal(result, manual)

