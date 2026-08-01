
def test_hash_keys():
    # Using different hash keys, should have
    # different hashes for the same data.
    #
    # This only matters for object dtypes.
    obj = Series(list("abc"))

    a = hash_pandas_object(obj, hash_key="9876543210123456")
    b = hash_pandas_object(obj, hash_key="9876543210123465")

    assert (a != b).all()

