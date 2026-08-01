
def test_already_encoded(index):
    # If already encoded, then ok.
    obj = Series(list("abc")).str.encode("utf8")
    a = hash_pandas_object(obj, index=index)
    b = hash_pandas_object(obj, index=index)
    tm.assert_series_equal(a, b)

