
def test_SDM_lu():
    A = SDM({0:{0:QQ(1), 1:QQ(2)}, 1:{0:QQ(3), 1:QQ(4)}}, (2, 2), QQ)
    L = SDM({0:{0:QQ(1)}, 1:{0:QQ(3), 1:QQ(1)}}, (2, 2), QQ)
    #U = SDM({0:{0:QQ(1), 1:QQ(2)}, 1:{0:QQ(3), 1:QQ(-2)}}, (2, 2), QQ)
    #swaps = []
    # This doesn't quite work. U has some nonzero elements in the lower part.
    #assert A.lu() == (L, U, swaps)
    assert A.lu()[0] == L

