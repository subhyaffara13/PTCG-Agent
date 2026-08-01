
def test_level_setting_resets_attributes():
    ind = MultiIndex.from_arrays([["A", "A", "B", "B", "B"], [1, 2, 1, 2, 3]])
    assert ind.is_monotonic_increasing
    ind = ind.set_levels([["A", "B"], [1, 3, 2]])
    # if this fails, probably didn't reset the cache correctly.
    assert not ind.is_monotonic_increasing

