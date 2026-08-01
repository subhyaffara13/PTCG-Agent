
def test_indexing_unordered2():
    # diff freq
    rng = date_range(datetime(2005, 1, 1), periods=20, freq="ME")
    ts = Series(np.arange(len(rng)), index=rng)
    ts = ts.take(np.random.default_rng(2).permutation(20))

    result = ts["2005"]
    for t in result.index:
        assert t.year == 2005

