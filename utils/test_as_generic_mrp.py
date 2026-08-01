
def test_as_generic_mrp(xp):
    quat = xp.asarray([
        [1, 2, -1, 0.5],
        [1, -1, 1, 0.0003],
        [0, 0, 0, 1]])
    quat /= xp_vector_norm(quat, axis=1)[:, None]

    expected_mrp = xp.asarray([
        [0.33333333, 0.66666667, -0.33333333],
        [0.57725028, -0.57725028, 0.57725028],
        [0, 0, 0]])
    xp_assert_close(Rotation.from_quat(quat).as_mrp(), expected_mrp)

