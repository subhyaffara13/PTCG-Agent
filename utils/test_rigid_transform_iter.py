
def test_rigid_transform_iter(xp):
    r = rigid_transform_to_xp(RigidTransform.identity(3), xp)
    for i, r_i in enumerate(r):
        assert isinstance(r_i, RigidTransform)
        xp_assert_equal(r_i.as_matrix(), r[i].as_matrix())
        if i > len(r):
            raise RuntimeError("Iteration exceeded length of transforms")

