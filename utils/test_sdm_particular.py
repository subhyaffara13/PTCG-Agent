
def test_SDM_particular():
    A = SDM({0:{0:QQ(1)}}, (2, 2), QQ)
    Apart = SDM.zeros((1, 2), QQ)
    assert A.particular() == Apart

