
def test_XXM_det_QQ(DM):
    dM1 = DM([[(1,2), (2,3)], [(3,4), (4,5)]])
    assert dM1.det() == QQ(-1,10)

