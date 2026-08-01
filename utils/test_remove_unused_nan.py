
def test_remove_unused_nan(level0, level1):
    # GH 18417
    mi = MultiIndex(levels=[level0, level1], codes=[[0, 2, -1, 1, -1], [0, 1, 2, 3, 2]])

    result = mi.remove_unused_levels()
    tm.assert_index_equal(result, mi)
    for level in 0, 1:
        assert "unused" not in result.levels[level]

