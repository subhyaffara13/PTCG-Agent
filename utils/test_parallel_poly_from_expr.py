
def test_parallel_poly_from_expr():
    assert parallel_poly_from_expr(
        [x - 1, x**2 - 1], x)[0] == [Poly(x - 1, x), Poly(x**2 - 1, x)]
    assert parallel_poly_from_expr(
        [Poly(x - 1, x), x**2 - 1], x)[0] == [Poly(x - 1, x), Poly(x**2 - 1, x)]
    assert parallel_poly_from_expr(
        [x - 1, Poly(x**2 - 1, x)], x)[0] == [Poly(x - 1, x), Poly(x**2 - 1, x)]
    assert parallel_poly_from_expr([Poly(
        x - 1, x), Poly(x**2 - 1, x)], x)[0] == [Poly(x - 1, x), Poly(x**2 - 1, x)]

    assert parallel_poly_from_expr(
        [x - 1, x**2 - 1], x, y)[0] == [Poly(x - 1, x, y), Poly(x**2 - 1, x, y)]
    assert parallel_poly_from_expr([Poly(
        x - 1, x), x**2 - 1], x, y)[0] == [Poly(x - 1, x, y), Poly(x**2 - 1, x, y)]
    assert parallel_poly_from_expr([x - 1, Poly(
        x**2 - 1, x)], x, y)[0] == [Poly(x - 1, x, y), Poly(x**2 - 1, x, y)]
    assert parallel_poly_from_expr([Poly(x - 1, x), Poly(
        x**2 - 1, x)], x, y)[0] == [Poly(x - 1, x, y), Poly(x**2 - 1, x, y)]

    assert parallel_poly_from_expr(
        [x - 1, x**2 - 1])[0] == [Poly(x - 1, x), Poly(x**2 - 1, x)]
    assert parallel_poly_from_expr(
        [Poly(x - 1, x), x**2 - 1])[0] == [Poly(x - 1, x), Poly(x**2 - 1, x)]
    assert parallel_poly_from_expr(
        [x - 1, Poly(x**2 - 1, x)])[0] == [Poly(x - 1, x), Poly(x**2 - 1, x)]
    assert parallel_poly_from_expr(
        [Poly(x - 1, x), Poly(x**2 - 1, x)])[0] == [Poly(x - 1, x), Poly(x**2 - 1, x)]

    assert parallel_poly_from_expr(
        [1, x**2 - 1])[0] == [Poly(1, x), Poly(x**2 - 1, x)]
    assert parallel_poly_from_expr(
        [1, x**2 - 1])[0] == [Poly(1, x), Poly(x**2 - 1, x)]
    assert parallel_poly_from_expr(
        [1, Poly(x**2 - 1, x)])[0] == [Poly(1, x), Poly(x**2 - 1, x)]
    assert parallel_poly_from_expr(
        [1, Poly(x**2 - 1, x)])[0] == [Poly(1, x), Poly(x**2 - 1, x)]

    assert parallel_poly_from_expr(
        [x**2 - 1, 1])[0] == [Poly(x**2 - 1, x), Poly(1, x)]
    assert parallel_poly_from_expr(
        [x**2 - 1, 1])[0] == [Poly(x**2 - 1, x), Poly(1, x)]
    assert parallel_poly_from_expr(
        [Poly(x**2 - 1, x), 1])[0] == [Poly(x**2 - 1, x), Poly(1, x)]
    assert parallel_poly_from_expr(
        [Poly(x**2 - 1, x), 1])[0] == [Poly(x**2 - 1, x), Poly(1, x)]

    assert parallel_poly_from_expr([Poly(x, x, y), Poly(y, x, y)], x, y, order='lex')[0] == \
        [Poly(x, x, y, domain='ZZ'), Poly(y, x, y, domain='ZZ')]

    raises(PolificationFailed, lambda: parallel_poly_from_expr([0, 1]))

