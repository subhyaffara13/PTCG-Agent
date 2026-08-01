
def test_rotation_iter(xp):
    r = rotation_to_xp(Rotation.random(3), xp)
    for i, r_i in enumerate(r):
        assert isinstance(r_i, Rotation)
        xp_assert_equal(r_i.as_quat(), r[i].as_quat())
        if i > len(r):
            raise RuntimeError("Iteration exceeded length of rotations")

