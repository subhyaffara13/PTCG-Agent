
def test_left_outer_join():
    result = set(join(identity, [1, 2], identity, [2, 3], left_default=None))
    expected = {(2, 2), (None, 3)}

    assert result == expected

