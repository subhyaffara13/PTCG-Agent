
def test_hash_pandas_series(series, index):
    a = hash_pandas_object(series, index=index)
    b = hash_pandas_object(series, index=index)
    tm.assert_series_equal(a, b)

