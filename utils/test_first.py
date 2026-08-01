
def test_first():
    assert first is toolz.itertoolz.first


def test_first():
    assert first('ABCDE') == 'A'
    assert first((3, 2, 1)) == 3
    assert isinstance(first({0: 'zero', 1: 'one'}), int)

