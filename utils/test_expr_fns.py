
def test_expr_fns():
    expr = x + y**3
    e = bottom_up(lambda v: v + 1, expr_fns)(expr)
    b = bottom_up(lambda v: Basic.__new__(Add, v, S(1)), basic_fns)(expr)

    assert rebuild(b) == e

