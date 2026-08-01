
def test_usage_via_getsizeof():
    df = DataFrame(
        data=1, index=MultiIndex.from_product([["a"], range(1000)]), columns=["A"]
    )
    mem = df.memory_usage(deep=True).sum()
    # sys.getsizeof will call the .memory_usage with
    # deep=True, and add on some GC overhead
    diff = mem - sys.getsizeof(df)
    assert abs(diff) < 100

