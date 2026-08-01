
def test_Relationals():
    assert theq(aesara_code_(sy.Eq(x, y)), aet.eq(xt, yt))
    # assert theq(aesara_code_(sy.Ne(x, y)), aet.neq(xt, yt))  # TODO - implement
    assert theq(aesara_code_(x > y), xt > yt)
    assert theq(aesara_code_(x < y), xt < yt)
    assert theq(aesara_code_(x >= y), xt >= yt)
    assert theq(aesara_code_(x <= y), xt <= yt)


def test_Relationals():
    assert theq(theano_code_(sy.Eq(x, y)), tt.eq(xt, yt))
    # assert theq(theano_code_(sy.Ne(x, y)), tt.neq(xt, yt))  # TODO - implement
    assert theq(theano_code_(x > y), xt > yt)
    assert theq(theano_code_(x < y), xt < yt)
    assert theq(theano_code_(x >= y), xt >= yt)
    assert theq(theano_code_(x <= y), xt <= yt)

