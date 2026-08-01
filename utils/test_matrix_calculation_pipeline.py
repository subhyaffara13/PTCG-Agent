
def test_matrix_calculation_pipeline(xp):
    mat = xp.asarray(special_ortho_group.rvs(3, size=10, random_state=0))
    xp_assert_close(Rotation.from_matrix(mat).as_matrix(), mat)

