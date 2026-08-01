
def test_hash_tuples_err(val):
    msg = "must be convertible to a list-of-tuples"
    with pytest.raises(TypeError, match=msg):
        hash_tuples(val)

