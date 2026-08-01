
def test_hash_pandas_series_diff_index(series):
    a = hash_pandas_object(series, index=True)
    b = hash_pandas_object(series, index=False)
    assert not (a == b).all()

