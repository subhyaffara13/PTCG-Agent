
def test_decode_bad_dtype():
    # https://github.com/pandas-dev/pandas/pull/60940
    ser = Series([b"a", b"b"])
    msg = "dtype must be string or object, got dtype='int64'"
    with pytest.raises(ValueError, match=msg):
        ser.str.decode("utf-8", dtype="int64")

