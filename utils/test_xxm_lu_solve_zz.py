
def test_XXM_lu_solve_ZZ(DM):
    dM1 = DM([[1, 2, 3], [4, 5, 6], [7, 8, 10]])
    dM2 = DM([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    raises(DMDomainError, lambda: dM1.lu_solve(dM2))

