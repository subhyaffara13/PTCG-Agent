
def test_set_names_only_clears_level_cache():
    mi = MultiIndex.from_arrays([range(4), range(4)], names=["a", "b"])
    mi.dtypes
    mi.is_monotonic_increasing
    mi._engine
    mi.levels
    old_cache_keys = sorted(mi._cache.keys())
    assert old_cache_keys == ["_engine", "dtypes", "is_monotonic_increasing", "levels"]
    mi.names = ["A", "B"]
    new_cache_keys = sorted(mi._cache.keys())
    assert new_cache_keys == ["_engine", "dtypes", "is_monotonic_increasing"]
    new_levels = mi.levels
    tm.assert_index_equal(new_levels[0], RangeIndex(4, name="A"))
    tm.assert_index_equal(new_levels[1], RangeIndex(4, name="B"))

