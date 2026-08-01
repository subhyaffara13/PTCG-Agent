
def test_second():
    assert second('ABCDE') == 'B'
    assert second((3, 2, 1)) == 2
    assert isinstance(second({0: 'zero', 1: 'one'}), int)

