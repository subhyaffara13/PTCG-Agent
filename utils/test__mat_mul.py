
def test_MatMul():
    expr = X*Y*Z
    expr_t = aesara_code_(expr)
    assert isinstance(expr_t.owner.op, Dot)
    assert theq(expr_t, Xt.dot(Yt).dot(Zt))


def test_MatMul():
    expr = X*Y*Z
    expr_t = theano_code_(expr)
    assert isinstance(expr_t.owner.op, tt.Dot)
    assert theq(expr_t, Xt.dot(Yt).dot(Zt))

