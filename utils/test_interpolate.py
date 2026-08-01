
def test_interpolate():
    assert interpolate([1, 4, 9, 16], x) == x**2
    assert interpolate([1, 4, 9, 25], x) == S(3)*x**3/2 - S(8)*x**2 + S(33)*x/2 - 9
    assert interpolate([(1, 1), (2, 4), (3, 9)], x) == x**2
    assert interpolate([(1, 2), (2, 5), (3, 10)], x) == 1 + x**2
    assert interpolate({1: 2, 2: 5, 3: 10}, x) == 1 + x**2
    assert interpolate({5: 2, 7: 5, 8: 10, 9: 13}, x) == \
        -S(13)*x**3/24 + S(12)*x**2 - S(2003)*x/24 + 187
    assert interpolate([(1, 3), (0, 6), (2, 5), (5, 7), (-2, 4)], x) == \
        S(-61)*x**4/280 + S(247)*x**3/210 + S(139)*x**2/280 - S(1871)*x/420 + 6
    assert interpolate((9, 4, 9), 3) == 9
    assert interpolate((1, 9, 16), 1) is S.One
    assert interpolate(((x, 1), (2, 3)), x) is S.One
    assert interpolate({x: 1, 2: 3}, x) is S.One
    assert interpolate(((2, x), (1, 3)), x) == x**2 - 4*x + 6

