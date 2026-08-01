
def test_int_raise_missing_values(indexer):
    arr = np.array([1, 2, 3])

    msg = "Cannot index with an integer indexer containing NA values"
    with pytest.raises(ValueError, match=msg):
        check_array_indexer(arr, indexer)

