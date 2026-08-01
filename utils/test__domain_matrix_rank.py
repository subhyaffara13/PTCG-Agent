
def test_DomainMatrix_rank():
    A = DomainMatrix([[QQ(1), QQ(2)], [QQ(3), QQ(4)], [QQ(6), QQ(8)]], (3, 2), QQ)
    assert A.rank() == 2

