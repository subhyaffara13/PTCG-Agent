
def test_value_counts_index_datetimelike(index, expected_index):
    vc = index.value_counts(sort=False, dropna=False)
    tm.assert_index_equal(vc.index, expected_index)

