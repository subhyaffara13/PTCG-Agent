
def test_factor_system_cond():

    assert factor_system_cond([x ** 2 - 1, x ** 2 - 4]) == [
        [x + 2, x + 1],
        [x + 2, x - 1],
        [x + 1, x - 2],
        [x - 1, x - 2],
    ]

    assert factor_system_cond([1]) == []
    assert factor_system_cond([0]) == [[]]
    assert factor_system_cond([1, x]) == []
    assert factor_system_cond([0, x]) == [[x]]
    assert factor_system_cond([]) == [[]]

    assert factor_system_cond([x**2 + y*x]) == [[x + y], [x]]

    assert factor_system_cond([(a - 1)*(x - 2), (b - 3)*(x - 2)], [x]) == [
        [x - 2],
        [a - 1, b - 3],
    ]

    assert factor_system_cond([a * (x - 1), b], [x]) == [[x - 1, b], [a, b]]

    assert factor_system_cond([a*x*(x-1), b*y, c], [x, y]) == [
        [x - 1, y, c],
        [x, y, c],
        [x - 1, b, c],
        [x, b, c],
        [y, a, c],
        [a, b, c],
    ]

    assert factor_system_cond([x*(x-1), y], [x, y]) == [[x - 1, y], [x, y]]

    assert factor_system_cond([a*x, y, a], [x, y]) == [[y, a]]

    assert factor_system_cond([a*x, b*x], [x, y]) == [[x], [a, b]]

    assert factor_system_cond([a*b*x, y], [x, y]) == [[x, y], [y, a*b]]

    assert factor_system_cond([a*b*x, y]) == [[x, y], [y, a], [y, b]]

    assert factor_system_cond([a**2*x, y], [x, y]) == [[x, y], [y, a]]

