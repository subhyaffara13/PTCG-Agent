
def test_unpack():
    assert unpack(Basic(S(2))) == 2
    assert unpack(Basic(S(2), S(3))) == Basic(S(2), S(3))


def test_unpack():
    assert unpack(MatMul(A, evaluate=False)) == A
    x = MatMul(A, B)
    assert unpack(x) == x

