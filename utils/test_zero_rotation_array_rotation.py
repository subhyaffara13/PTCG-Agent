
def test_zero_rotation_array_rotation(xp):
    r = Rotation.from_quat(xp.zeros((0, 4)))

    v = xp.asarray([1, 2, 3])
    v_rotated = r.apply(v)
    assert v_rotated.shape == (0, 3)

    v0 = xp.zeros((0, 3))
    v0_rot = r.apply(v0)
    assert v0_rot.shape == (0, 3)

    v2 = xp.ones((2, 3))
    with pytest.raises(
        ValueError, match="Cannot broadcast"):
        r.apply(v2)

