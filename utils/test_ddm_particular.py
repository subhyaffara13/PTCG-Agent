
def test_DDM_particular():
    A = DDM([[QQ(1), QQ(0)]], (1, 2), QQ)
    assert A.particular() == DDM.zeros((1, 1), QQ)

