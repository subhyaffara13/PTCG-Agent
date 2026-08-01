
def test_as_expr_variables():
    assert Order(x).as_expr_variables(None) == (x, ((x, 0),))
    assert Order(x).as_expr_variables(((x, 0),)) == (x, ((x, 0),))
    assert Order(y).as_expr_variables(((x, 0),)) == (y, ((x, 0), (y, 0)))
    assert Order(y).as_expr_variables(((x, 0), (y, 0))) == (y, ((x, 0), (y, 0)))

