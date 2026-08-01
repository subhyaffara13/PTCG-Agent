
def test_reusability():
    f = evaluate(False)

    with f:
        expr = x + x
        assert expr.args == (x, x)

    expr = x + x
    assert expr.args == (2, x)

    with f:
        expr = x + x
        assert expr.args == (x, x)

    # Assure reentrancy with reusability
    ctx = evaluate(False)
    with ctx:
        expr = x + x
        assert expr.args == (x, x)
        with ctx:
            expr = x + x
            assert expr.args == (x, x)

    expr = x + x
    assert expr.args == (2, x)

