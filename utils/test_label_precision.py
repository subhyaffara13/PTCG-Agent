
def test_label_precision():
    arr = np.arange(0, 0.73, 0.01)
    result = cut(arr, 4, precision=2)

    ex_levels = IntervalIndex.from_breaks([-0.00072, 0.18, 0.36, 0.54, 0.72])
    tm.assert_index_equal(result.categories, ex_levels)

