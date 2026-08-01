
def test_approx_equal_single_rotation(xp):
    # also tests passing single argument to approx_equal
    p = Rotation.from_rotvec(xp.asarray([0, 0, 1e-9]))  # less than default atol of 1e-8
    q = Rotation.from_quat(xp.eye(4))
    assert p.approx_equal(q[3])
    assert not p.approx_equal(q[0])
    # Regression test for gh-24769: single approx_equal should return a bool
    assert isinstance(p.approx_equal(q[0]), np.bool_) or not is_numpy(xp)

    # test passing atol and using degrees
    assert not p.approx_equal(q[3], atol=1e-10)
    assert not p.approx_equal(q[3], atol=1e-8, degrees=True)
    with pytest.warns(UserWarning, match="atol must be set"):
        assert p.approx_equal(q[3], degrees=True)

