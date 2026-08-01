
def test_df_encoding():
    # Check that DataFrame recognizes optional encoding.
    # https://github.com/pandas-dev/pandas/issues/41404
    # https://github.com/pandas-dev/pandas/pull/42049
    obj = DataFrame({"x": np.arange(3), "y": list("a+c")})

    a = hash_pandas_object(obj, encoding="utf8")
    b = hash_pandas_object(obj, encoding="utf7")

    # Note that the "+" is encoded as "+-" in utf-7.
    assert a[0] == b[0]
    assert a[1] != b[1]
    assert a[2] == b[2]

