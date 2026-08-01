
def test_construct_from_string(string, expected):
    result = SparseDtype.construct_from_string(string)
    assert result == expected

