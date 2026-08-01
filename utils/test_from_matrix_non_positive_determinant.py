
def test_from_matrix_non_positive_determinant(xp):
    mat = xp.eye(3)
    mat = xpx.at(mat)[0, 0].set(0)
    if is_lazy_array(mat):
        assert xp.all(xp.isnan(Rotation.from_matrix(mat).as_matrix()))
    else:
        with pytest.raises(ValueError, match="Non-positive determinant"):
            Rotation.from_matrix(mat)

    mat = xpx.at(mat)[0, 0].set(-1)
    if is_lazy_array(mat):
        assert xp.all(xp.isnan(Rotation.from_matrix(mat).as_matrix()))
    else:
        with pytest.raises(ValueError, match="Non-positive determinant"):
            Rotation.from_matrix(mat)

