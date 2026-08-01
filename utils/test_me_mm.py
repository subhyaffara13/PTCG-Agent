
def test_ME_MM():
    assert isinstance(Identity(3) + MM, MatrixExpr)
    assert isinstance(SM + MM, MatAdd)
    assert isinstance(MM + SM, MatAdd)
    assert (Identity(3) + MM)[1, 1] == 6

