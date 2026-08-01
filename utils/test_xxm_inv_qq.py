
def test_XXM_inv_QQ(DM):
    dM1 = DM([[(1,2), (2,3)], [(3,4), (4,5)]])
    dM2 = DM([[(-8,1), (20,3)], [(15,2), (-5,1)]])
    assert dM1.inv() == dM2
    assert dM1.matmul(dM2) == DM([[1, 0], [0, 1]])

    dM3 = DM([[(1,2), (2,3)], [(1,4), (1,3)]])
    raises(DMNonInvertibleMatrixError, lambda: dM3.inv())

    dM4 = DM([[(1,2), (2,3), (3,4)], [(1,4), (1,3), (1,2)]])
    raises(DMNonSquareMatrixError, lambda: dM4.inv())

