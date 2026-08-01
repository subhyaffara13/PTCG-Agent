
def test_as_mrp_single_nd_input(xp, ndim: int):
    quat = xp.asarray([1, 2, -3, 2])
    quat = xp.reshape(quat, (1,) * (ndim - 1) + (4,))
    expected_mrp = xp.asarray([0.16018862, 0.32037724, -0.48056586])
    expected_mrp = xp.reshape(expected_mrp, (1,) * (ndim - 1) + (3,))
    actual_mrp = Rotation.from_quat(quat).as_mrp()

    assert_equal(actual_mrp.shape, expected_mrp.shape)
    xp_assert_close(actual_mrp, expected_mrp)

