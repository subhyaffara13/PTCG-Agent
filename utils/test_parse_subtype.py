
def test_parse_subtype(string, expected):
    subtype, _ = SparseDtype._parse_subtype(string)
    assert subtype == expected

