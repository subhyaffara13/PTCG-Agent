
def test_df_hash_keys():
    # DataFrame version of the test_hash_keys.
    # https://github.com/pandas-dev/pandas/issues/41404
    obj = DataFrame({"x": np.arange(3), "y": list("abc")})

    a = hash_pandas_object(obj, hash_key="9876543210123456")
    b = hash_pandas_object(obj, hash_key="9876543210123465")

    assert (a != b).all()

