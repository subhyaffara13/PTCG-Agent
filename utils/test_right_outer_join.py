
def test_right_outer_join():
    result = set(join(identity, [1, 2], identity, [2, 3], right_default=None))
    expected = {(2, 2), (1, None)}

    assert result == expected

