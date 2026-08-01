
def test_from_mrp_single_nd_input(xp, ndim: int):
    mrp = xp.asarray([0, 0, 1.0])
    mrp = xp.reshape(mrp, (1,) * (ndim - 1) + (3,))
    expected_quat = xp.asarray([0.0, 0, 1, 0])
    expected_quat = xp.reshape(expected_quat, (1,) * (ndim - 1) + (4,))
    result = Rotation.from_mrp(mrp)
    xp_assert_close(result.as_quat(), expected_quat, atol=1e-12)
    # Regression test for gh-24555
    assert isinstance(result._quat, type(array_namespace(mrp).empty(0)))

