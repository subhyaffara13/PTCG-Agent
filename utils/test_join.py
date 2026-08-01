
def test_join():
    names = [(1, 'one'), (2, 'two'), (3, 'three')]
    fruit = [('apple', 1), ('orange', 1), ('banana', 2), ('coconut', 2)]

    def addpair(pair):
        return pair[0] + pair[1]

    result = set(starmap(add, join(first, names, second, fruit)))

    expected = {(1, 'one', 'apple', 1),
                    (1, 'one', 'orange', 1),
                    (2, 'two', 'banana', 2),
                    (2, 'two', 'coconut', 2)}

    assert result == expected

    result = set(starmap(add, join(first, names, second, fruit,
                                   left_default=no_default2,
                                   right_default=no_default2)))
    assert result == expected


def test_join(how, sort, expected):
    left = DataFrame({"a": [20, 10, 0]}, index=[2, 1, 0])
    right = DataFrame({"b": [300, 100, 200]}, index=[3, 1, 2])
    result = left.join(right, how=how, sort=sort, validate="1:1")
    tm.assert_frame_equal(result, expected)

