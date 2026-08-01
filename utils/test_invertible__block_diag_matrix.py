
def test_invertible_BlockDiagMatrix():
    assert ask(Q.invertible(BlockDiagMatrix(Identity(3), Identity(5)))) == True
    assert ask(Q.invertible(BlockDiagMatrix(ZeroMatrix(3, 3), Identity(5)))) == False
    assert ask(Q.invertible(BlockDiagMatrix(Identity(3), OneMatrix(5, 5)))) == False

