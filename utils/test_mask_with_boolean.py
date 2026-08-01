
def test_mask_with_boolean(index):
    ser = Series(range(3))
    idx = Categorical([True, False, True])
    if index:
        idx = CategoricalIndex(idx)

    assert com.is_bool_indexer(idx)
    result = ser[idx]
    expected = ser[idx.astype("object")]
    tm.assert_series_equal(result, expected)

