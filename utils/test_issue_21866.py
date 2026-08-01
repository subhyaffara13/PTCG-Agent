
def test_issue_21866():
    n  = 10
    I  = Identity(n)
    O  = ZeroMatrix(n, n)
    A  = BlockMatrix([[  I,  O,  O,  O ],
                      [  O,  I,  O,  O ],
                      [  O,  O,  I,  O ],
                      [  I,  O,  O,  I ]])
    Ainv = block_collapse(A.inv())
    AinvT = BlockMatrix([[  I,  O,  O,  O ],
                      [  O,  I,  O,  O ],
                      [  O,  O,  I,  O ],
                      [  -I,  O,  O,  I ]])
    assert Ainv == AinvT

