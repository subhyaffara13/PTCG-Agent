
def test_hash_pandas_object_diff_index_non_empty(obj):
    a = hash_pandas_object(obj, index=True)
    b = hash_pandas_object(obj, index=False)
    assert not (a == b).all()

