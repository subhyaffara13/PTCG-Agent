
def test_join_missing_element():
    names = [(1, 'one'), (2, 'two'), (3, 'three')]
    fruit = [('apple', 5), ('orange', 1)]

    result = set(starmap(add, join(first, names, second, fruit)))

    expected = {(1, 'one', 'orange', 1)}

    assert result == expected

