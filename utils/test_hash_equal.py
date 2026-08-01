
def test_hash_equal(a, b, expected):
    result = a == b
    assert result is expected

    result = hash(a) == hash(b)
    assert result is expected

