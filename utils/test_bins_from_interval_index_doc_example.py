
def test_bins_from_interval_index_doc_example():
    # Make sure we preserve the bins.
    ages = np.array([10, 15, 13, 12, 23, 25, 28, 59, 60])
    c = cut(ages, bins=[0, 18, 35, 70])
    expected = IntervalIndex.from_tuples([(0, 18), (18, 35), (35, 70)])
    tm.assert_index_equal(c.categories, expected)

    result = cut([25, 20, 50], bins=c.categories)
    tm.assert_index_equal(result.categories, expected)
    tm.assert_numpy_array_equal(result.codes, np.array([1, 1, 2], dtype="int8"))

