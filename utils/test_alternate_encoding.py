
def test_alternate_encoding(index):
    obj = Series(list("abc"))
    a = hash_pandas_object(obj, index=index)
    b = hash_pandas_object(obj, index=index)
    tm.assert_series_equal(a, b)

