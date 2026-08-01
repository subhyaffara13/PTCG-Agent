
def test_rotations():
    assert list(rotations('ab')) == [['a', 'b'], ['b', 'a']]
    assert list(rotations(range(3))) == [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
    assert list(rotations(range(3), dir=-1)) == [[0, 1, 2], [2, 0, 1], [1, 2, 0]]

