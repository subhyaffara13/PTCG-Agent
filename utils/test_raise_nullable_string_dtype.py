
def test_raise_nullable_string_dtype(nullable_string_dtype):
    indexer = pd.array(["a", "b"], dtype=nullable_string_dtype)
    arr = np.array([1, 2, 3])

    msg = "arrays used as indices must be of integer or boolean type"
    with pytest.raises(IndexError, match=msg):
        check_array_indexer(arr, indexer)

