
def test_outer_join():
    result = set(join(identity, [1, 2], identity, [2, 3],
                      left_default=None, right_default=None))
    expected = {(2, 2), (1, None), (None, 3)}

    assert result == expected

