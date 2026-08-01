
def test_last():
    assert last('ABCDE') == 'E'
    assert last((3, 2, 1)) == 1
    assert isinstance(last({0: 'zero', 1: 'one'}), int)

