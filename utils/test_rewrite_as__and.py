
def test_rewrite_as_And():
    expr = x ^ y
    assert expr.rewrite(And) == (x | y) & (~x | ~y)

