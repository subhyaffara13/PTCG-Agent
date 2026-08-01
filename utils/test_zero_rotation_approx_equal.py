
def test_zero_rotation_approx_equal(xp):
    r = Rotation.from_quat(xp.zeros((0, 4)))
    r0 = Rotation.from_quat(xp.zeros((0, 4)))
    assert r.approx_equal(r0).shape == (0,)
    r1 = Rotation.from_quat(xp.asarray([0.0, 0, 0, 1]))
    assert r.approx_equal(r1).shape == (0,)
    r2 = rotation_to_xp(Rotation.random(), xp)
    assert r2.approx_equal(r).shape == (0,)

    approx_msg = "Expected broadcastable shapes in both rotations"
    r3 = rotation_to_xp(Rotation.random(2), xp)
    with pytest.raises(ValueError, match=approx_msg):
        r.approx_equal(r3)

    with pytest.raises(ValueError, match=approx_msg):
        r3.approx_equal(r)

