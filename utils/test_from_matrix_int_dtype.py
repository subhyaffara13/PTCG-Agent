
def test_from_matrix_int_dtype(xp):
    mat = xp.asarray([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    r = Rotation.from_matrix(mat)
    assert r.as_quat().dtype == xp_default_dtype(xp)

