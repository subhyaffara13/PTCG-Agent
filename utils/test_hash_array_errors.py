
def test_hash_array_errors(val):
    msg = "must pass an ndarray-like"
    with pytest.raises(TypeError, match=msg):
        hash_array(val)

