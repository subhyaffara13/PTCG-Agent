
def test_pass_through_non_array_likes(indexer):
    arr = np.array([1, 2, 3])

    result = check_array_indexer(arr, indexer)
    assert result == indexer

