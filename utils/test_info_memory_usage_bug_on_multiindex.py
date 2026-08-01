
def test_info_memory_usage_bug_on_multiindex():
    # GH 14308
    # memory usage introspection should not materialize .values
    N = 100
    M = len(ascii_uppercase)
    index = MultiIndex.from_product(
        [list(ascii_uppercase), date_range("20160101", periods=N)],
        names=["id", "date"],
    )
    s = Series(np.random.default_rng(2).standard_normal(N * M), index=index)

    unstacked = s.unstack("id")
    assert s.values.nbytes == unstacked.values.nbytes
    assert s.memory_usage(deep=True) > unstacked.memory_usage(deep=True).sum()

    # high upper bound
    diff = unstacked.memory_usage(deep=True).sum() - s.memory_usage(deep=True)
    assert diff < 2000


def test_info_memory_usage_bug_on_multiindex():
    # GH 14308
    # memory usage introspection should not materialize .values

    def memory_usage(f):
        return f.memory_usage(deep=True).sum()

    N = 100
    M = len(ascii_uppercase)
    index = MultiIndex.from_product(
        [list(ascii_uppercase), date_range("20160101", periods=N)],
        names=["id", "date"],
    )
    df = DataFrame(
        {"value": np.random.default_rng(2).standard_normal(N * M)}, index=index
    )

    unstacked = df.unstack("id")
    assert df.values.nbytes == unstacked.values.nbytes
    assert memory_usage(df) > memory_usage(unstacked)

    # high upper bound
    assert memory_usage(unstacked) - memory_usage(df) < 2000

