
def test_rank_apply():
    lev1 = np.array(["a" * 10] * 100, dtype=object)
    lev2 = np.array(["b" * 10] * 130, dtype=object)
    lab1 = np.random.default_rng(2).integers(0, 100, size=500, dtype=int)
    lab2 = np.random.default_rng(2).integers(0, 130, size=500, dtype=int)

    df = DataFrame(
        {
            "value": np.random.default_rng(2).standard_normal(500),
            "key1": lev1.take(lab1),
            "key2": lev2.take(lab2),
        }
    )

    result = df.groupby(["key1", "key2"]).value.rank()

    expected = [piece.value.rank() for key, piece in df.groupby(["key1", "key2"])]
    expected = concat(expected, axis=0)
    expected = expected.reindex(result.index)
    tm.assert_series_equal(result, expected)

    result = df.groupby(["key1", "key2"]).value.rank(pct=True)

    expected = [
        piece.value.rank(pct=True) for key, piece in df.groupby(["key1", "key2"])
    ]
    expected = concat(expected, axis=0)
    expected = expected.reindex(result.index)
    tm.assert_series_equal(result, expected)

