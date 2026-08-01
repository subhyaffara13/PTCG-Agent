
def test_reentrantcy():
    with evaluate(False):
        expr = x + x
        assert expr.args == (x, x)
        with evaluate(True):
            expr = x + x
            assert expr.args == (2, x)
        expr = x + x
        assert expr.args == (x, x)

