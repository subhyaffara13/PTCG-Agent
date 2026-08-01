
def test__dict_from_expr_no_gens():
    assert dict_from_expr(Integer(17)) == ({(): Integer(17)}, ())

    assert dict_from_expr(x) == ({(1,): Integer(1)}, (x,))
    assert dict_from_expr(y) == ({(1,): Integer(1)}, (y,))

    assert dict_from_expr(x*y) == ({(1, 1): Integer(1)}, (x, y))
    assert dict_from_expr(
        x + y) == ({(1, 0): Integer(1), (0, 1): Integer(1)}, (x, y))

    assert dict_from_expr(sqrt(2)) == ({(1,): Integer(1)}, (sqrt(2),))
    assert dict_from_expr(sqrt(2), greedy=False) == ({(): sqrt(2)}, ())

    assert dict_from_expr(x*y, domain=ZZ[x]) == ({(1,): x}, (y,))
    assert dict_from_expr(x*y, domain=ZZ[y]) == ({(1,): y}, (x,))

    assert dict_from_expr(3*sqrt(
        2)*pi*x*y, extension=None) == ({(1, 1, 1, 1): 3}, (x, y, pi, sqrt(2)))
    assert dict_from_expr(3*sqrt(
        2)*pi*x*y, extension=True) == ({(1, 1, 1): 3*sqrt(2)}, (x, y, pi))

    assert dict_from_expr(3*sqrt(
        2)*pi*x*y, extension=True) == ({(1, 1, 1): 3*sqrt(2)}, (x, y, pi))

    f = cos(x)*sin(x) + cos(x)*sin(y) + cos(y)*sin(x) + cos(y)*sin(y)

    assert dict_from_expr(f) == ({(0, 1, 0, 1): 1, (0, 1, 1, 0): 1,
        (1, 0, 0, 1): 1, (1, 0, 1, 0): 1}, (cos(x), cos(y), sin(x), sin(y)))

