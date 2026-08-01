
def test_parallel_dict_from_expr():
    assert parallel_dict_from_expr([Eq(x, 1), Eq(
        x**2, 2)]) == ([{(0,): -Integer(1), (1,): Integer(1)},
                        {(0,): -Integer(2), (2,): Integer(1)}], (x,))
    raises(PolynomialError, lambda: parallel_dict_from_expr([A*B - B*A]))

