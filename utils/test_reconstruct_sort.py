
def test_reconstruct_sort():
    # starts off lexsorted & monotonic
    mi = MultiIndex.from_arrays([["A", "A", "B", "B", "B"], [1, 2, 1, 2, 3]])
    assert mi.is_monotonic_increasing
    recons = mi._sort_levels_monotonic()
    assert recons.is_monotonic_increasing
    assert mi is recons

    assert mi.equals(recons)
    assert Index(mi.values).equals(Index(recons.values))

    # cannot convert to lexsorted
    mi = MultiIndex.from_tuples(
        [("z", "a"), ("x", "a"), ("y", "b"), ("x", "b"), ("y", "a"), ("z", "b")],
        names=["one", "two"],
    )
    assert not mi.is_monotonic_increasing
    recons = mi._sort_levels_monotonic()
    assert not recons.is_monotonic_increasing
    assert mi.equals(recons)
    assert Index(mi.values).equals(Index(recons.values))

    # cannot convert to lexsorted
    mi = MultiIndex(
        levels=[["b", "d", "a"], [1, 2, 3]],
        codes=[[0, 1, 0, 2], [2, 0, 0, 1]],
        names=["col1", "col2"],
    )
    assert not mi.is_monotonic_increasing
    recons = mi._sort_levels_monotonic()
    assert not recons.is_monotonic_increasing
    assert mi.equals(recons)
    assert Index(mi.values).equals(Index(recons.values))

