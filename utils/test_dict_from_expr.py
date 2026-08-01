
def test_dict_from_expr():
    assert dict_from_expr(Eq(x, 1)) == \
        ({(0,): -Integer(1), (1,): Integer(1)}, (x,))
    raises(PolynomialError, lambda: dict_from_expr(A*B - B*A))
    raises(PolynomialError, lambda: dict_from_expr(S.true))

