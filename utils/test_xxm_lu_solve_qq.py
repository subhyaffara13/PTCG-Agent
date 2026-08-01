
def test_XXM_lu_solve_QQ(DM):
    dM1 = DM([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
    dM2 = DM([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    dM3 = DM([[(-2,3),(-4,3),(1,1)],[(-2,3),(11,3),(-2,1)],[(1,1),(-2,1),(1,1)]])
    assert dM1.lu_solve(dM2) == dM3 == dM1.inv()

    dM4 = DM([[1, 2, 3], [4, 5, 6]])
    dM5 = DM([[1, 0], [0, 1], [0, 0]])
    raises(DMShapeError, lambda: dM4.lu_solve(dM5))

