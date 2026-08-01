
def _assert_equal_hash(v1, v2):
    assert v1 == v2
    assert hash(v1) == hash(v2)
    assert v2 in {v1}

