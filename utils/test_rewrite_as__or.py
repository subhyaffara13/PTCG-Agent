
def test_rewrite_as_Or():
    expr = x ^ y
    assert expr.rewrite(Or) == (x & ~y) | (y & ~x)

