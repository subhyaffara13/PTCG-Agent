
def test__partition():
    assert _partition('abcde', [1, 0, 1, 2, 0]) == [
        ['b', 'e'], ['a', 'c'], ['d']]
    assert _partition('abcde', [1, 0, 1, 2, 0], 3) == [
        ['b', 'e'], ['a', 'c'], ['d']]
    output = (3, [1, 0, 1, 2, 0])
    assert _partition('abcde', *output) == [['b', 'e'], ['a', 'c'], ['d']]


def test_Partition():
    assert str(Partition(FiniteSet(x, y), {z})) == 'Partition({z}, {x, y})'


def test__partition():
    assert [_partition(k) for k in range(13)] == \
        [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77]
    assert _partition(100) == 190569292
    assert _partition(200) == 3972999029388
    assert _partition(1000) == 24061467864032622473692149727991
    assert _partition(1001) == 25032297938763929621013218349796
    assert _partition(2000) == 4720819175619413888601432406799959512200344166
    assert _partition(10000) % 10**10 == 6916435144
    assert _partition(100000) % 10**10 == 9421098519
    assert _partition(10000000) % 10**10 == 7677288980

