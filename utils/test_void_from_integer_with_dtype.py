
def test_void_from_integer_with_dtype(data):
    # The "length" meaning is ignored, rather data is used:
    res = np.void(data, dtype="i,i")
    assert type(res) is np.void
    assert res.dtype == "i,i"
    assert res["f0"] == 5 and res["f1"] == 5

