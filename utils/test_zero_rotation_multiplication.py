
def test_zero_rotation_multiplication(xp):
    r = Rotation.from_quat(xp.zeros((0, 4)))

    r_single = Rotation.from_quat(xp.asarray([0.0, 0, 0, 1]))
    r_mult_left = r * r_single
    assert len(r_mult_left) == 0

    r_mult_right = r_single * r
    assert len(r_mult_right) == 0

    r0 = Rotation.from_quat(xp.zeros((0, 4)))
    r_mult = r * r0
    assert len(r_mult) == 0

    r2 = rotation_to_xp(Rotation.random(2), xp)
    with pytest.raises(ValueError, match="Cannot broadcast"):
        r0 * r2

    with pytest.raises(ValueError, match="Cannot broadcast"):
        r2 * r0

