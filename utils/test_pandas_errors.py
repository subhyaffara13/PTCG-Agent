
def test_pandas_errors():
    msg = "Unexpected type for hashing"
    with pytest.raises(TypeError, match=msg):
        hash_pandas_object(pd.Timestamp("20130101"))

