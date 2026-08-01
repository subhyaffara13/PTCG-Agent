
def test_join_double_repeats():
    names = [(1, 'one'), (2, 'two'), (3, 'three'), (1, 'uno'), (2, 'dos')]
    fruit = [('apple', 1), ('orange', 1), ('banana', 2), ('coconut', 2)]

    result = set(starmap(add, join(first, names, second, fruit)))

    expected = {(1, 'one', 'apple', 1),
                    (1, 'one', 'orange', 1),
                    (2, 'two', 'banana', 2),
                    (2, 'two', 'coconut', 2),
                    (1, 'uno', 'apple', 1),
                    (1, 'uno', 'orange', 1),
                    (2, 'dos', 'banana', 2),
                    (2, 'dos', 'coconut', 2)}

    assert result == expected

