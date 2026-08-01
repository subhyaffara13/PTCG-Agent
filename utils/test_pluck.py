
def test_pluck():
    assert list(pluck(0, [[0, 1], [2, 3], [4, 5]])) == [0, 2, 4]
    assert list(pluck([0, 1], [[0, 1, 2], [3, 4, 5]])) == [(0, 1), (3, 4)]
    assert list(pluck(1, [[0], [0, 1]], None)) == [None, 1]

    data = [{'id': 1, 'name': 'cheese'}, {'id': 2, 'name': 'pies', 'price': 1}]
    assert list(pluck('id', data)) == [1, 2]
    assert list(pluck('price', data, 0)) == [0, 1]
    assert list(pluck(['id', 'name'], data)) == [(1, 'cheese'), (2, 'pies')]
    assert list(pluck(['name'], data)) == [('cheese',), ('pies',)]
    assert list(pluck(['price', 'other'], data, 0)) == [(0, 0), (1, 0)]

    assert raises(IndexError, lambda: list(pluck(1, [[0]])))
    assert raises(KeyError, lambda: list(pluck('name', [{'id': 1}])))

    assert list(pluck(0, [[0, 1], [2, 3], [4, 5]], no_default2)) == [0, 2, 4]
    assert raises(IndexError, lambda: list(pluck(1, [[0]], no_default2)))

