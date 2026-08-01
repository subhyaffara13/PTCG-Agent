
def test_has_duplicates(idx, idx_dup):
    # see fixtures
    assert idx.is_unique is True
    assert idx.has_duplicates is False
    assert idx_dup.is_unique is False
    assert idx_dup.has_duplicates is True

    mi = MultiIndex(
        levels=[[0, 1], [0, 1, 2]], codes=[[0, 0, 0, 0, 1, 1, 1], [0, 1, 2, 0, 0, 1, 2]]
    )
    assert mi.is_unique is False
    assert mi.has_duplicates is True

    # single instance of NaN
    mi_nan = MultiIndex(
        levels=[["a", "b"], [0, 1]], codes=[[-1, 0, 0, 1, 1], [-1, 0, 1, 0, 1]]
    )
    assert mi_nan.is_unique is True
    assert mi_nan.has_duplicates is False

    # multiple instances of NaN
    mi_nan_dup = MultiIndex(
        levels=[["a", "b"], [0, 1]], codes=[[-1, -1, 0, 0, 1, 1], [-1, -1, 0, 1, 0, 1]]
    )
    assert mi_nan_dup.is_unique is False
    assert mi_nan_dup.has_duplicates is True

