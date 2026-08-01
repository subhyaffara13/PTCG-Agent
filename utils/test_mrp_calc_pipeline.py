
def test_mrp_calc_pipeline(xp):
    actual_mrp = xp.asarray([
        [0, 0, 0],
        [1, -1, 2],
        [0.41421356, 0, 0],
        [0.1, 0.2, 0.1]])
    expected_mrp = xp.asarray([
        [0, 0, 0],
        [-0.16666667, 0.16666667, -0.33333333],
        [0.41421356, 0, 0],
        [0.1, 0.2, 0.1]])
    xp_assert_close(Rotation.from_mrp(actual_mrp).as_mrp(), expected_mrp)

