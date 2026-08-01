
def test_symbols_are_created_once():
    """
    Test that a symbol is cached and reused when it appears in an expression
    more than once.
    """
    expr = sy.Add(x, x, evaluate=False)
    comp = aesara_code_(expr)

    assert theq(comp, xt + xt)
    assert not theq(comp, xt + aesara_code_(x))


def test_symbols_are_created_once():
    """
    Test that a symbol is cached and reused when it appears in an expression
    more than once.
    """
    expr = sy.Add(x, x, evaluate=False)
    comp = theano_code_(expr)

    assert theq(comp, xt + xt)
    assert not theq(comp, xt + theano_code_(x))

