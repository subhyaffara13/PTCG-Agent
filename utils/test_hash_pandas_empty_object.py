
def test_hash_pandas_empty_object(klass, dtype, index):
    # These are by-definition the same with
    # or without the index as the data is empty.
    obj = klass([], dtype=dtype)
    a = hash_pandas_object(obj, index=index)
    b = hash_pandas_object(obj, index=index)
    tm.assert_series_equal(a, b)

