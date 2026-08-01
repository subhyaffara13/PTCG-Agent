
def test_many():
    """ Test printing a complex expression with multiple symbols. """
    expr = sy.exp(x**2 + sy.cos(y)) * sy.log(2*z)
    comp = aesara_code_(expr)
    expected = aet.exp(xt**2 + aet.cos(yt)) * aet.log(2*zt)
    assert theq(comp, expected)


def test_many():
    """ Test printing a complex expression with multiple symbols. """
    expr = sy.exp(x**2 + sy.cos(y)) * sy.log(2*z)
    comp = theano_code_(expr)
    expected = tt.exp(xt**2 + tt.cos(yt)) * tt.log(2*zt)
    assert theq(comp, expected)

