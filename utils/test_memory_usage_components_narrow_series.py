
def test_memory_usage_components_narrow_series(any_real_numpy_dtype):
    series = Series(
        range(5),
        dtype=any_real_numpy_dtype,
        index=[f"i-{i}" for i in range(5)],
        name="a",
    )
    total_usage = series.memory_usage(index=True)
    non_index_usage = series.memory_usage(index=False)
    index_usage = series.index.memory_usage()
    assert total_usage == non_index_usage + index_usage

