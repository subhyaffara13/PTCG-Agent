
def test_maybe_match_name(left, right, expected):
    res = ops.common._maybe_match_name(left, right)
    assert res is expected or res == expected

