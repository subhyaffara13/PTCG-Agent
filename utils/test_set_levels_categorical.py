
def test_set_levels_categorical(ordered):
    # GH13854
    index = MultiIndex.from_arrays([list("xyzx"), [0, 1, 2, 3]])

    cidx = CategoricalIndex(list("bac"), ordered=ordered)
    result = index.set_levels(cidx, level=0)
    expected = MultiIndex(levels=[cidx, [0, 1, 2, 3]], codes=index.codes)
    tm.assert_index_equal(result, expected)

    result_lvl = result.get_level_values(0)
    expected_lvl = CategoricalIndex(
        list("bacb"), categories=cidx.categories, ordered=cidx.ordered
    )
    tm.assert_index_equal(result_lvl, expected_lvl)

