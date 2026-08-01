
def test_groups():
    many_to_one = dict(zip("abcde", [0, 0, 1, 1, 2]))
    actual = groups(many_to_one)
    expected = {0: {"a", "b"}, 1: {"c", "d"}, 2: {"e"}}
    assert actual == expected
    assert {} == groups({})

