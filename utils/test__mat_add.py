
def test_MatAdd():
    expr = X+Y+Z
    assert isinstance(aesara_code_(expr).owner.op, Elemwise)


def test_MatAdd():
    expr = X+Y+Z
    assert isinstance(theano_code_(expr).owner.op, tt.Elemwise)

