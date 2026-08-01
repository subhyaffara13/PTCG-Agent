
def test_example_symbols():
    """
    Check that the example symbols in this module print to their Aesara
    equivalents, as many of the other tests depend on this.
    """
    assert theq(xt, aesara_code_(x))
    assert theq(yt, aesara_code_(y))
    assert theq(zt, aesara_code_(z))
    assert theq(Xt, aesara_code_(X))
    assert theq(Yt, aesara_code_(Y))
    assert theq(Zt, aesara_code_(Z))


def test_example_symbols():
    """
    Check that the example symbols in this module print to their Theano
    equivalents, as many of the other tests depend on this.
    """
    assert theq(xt, theano_code_(x))
    assert theq(yt, theano_code_(y))
    assert theq(zt, theano_code_(z))
    assert theq(Xt, theano_code_(X))
    assert theq(Yt, theano_code_(Y))
    assert theq(Zt, theano_code_(Z))

