
def test_XXM_charpoly_QQ(DM):
    dM1 = DM([[(1,2), (2,3)], [(3,4), (4,5)]])
    assert dM1.charpoly() == [QQ(1,1), QQ(-13,10), QQ(-1,10)]

