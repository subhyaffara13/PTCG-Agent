
def test_from_as_internal_consistency(xp, ndim: int):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12
    n = 10
    rng = np.random.default_rng(10)
    shape = (n,) + (ndim,) * (ndim - 1)

    t = xp.asarray(rng.normal(size=shape + (3,)), dtype=dtype)
    r = Rotation.from_quat(xp.asarray(rng.normal(size=shape + (4,)), dtype=dtype))
    tf0 = RigidTransform.from_components(t, r)

    tf1 = RigidTransform.from_components(*tf0.as_components())
    xp_assert_close(tf0.as_matrix(), tf1.as_matrix(), atol=atol)

    tf1 = RigidTransform.from_components(tf0.translation, tf0.rotation)
    xp_assert_close(tf0.as_matrix(), tf1.as_matrix(), atol=atol)

    tf1 = RigidTransform.from_exp_coords(tf0.as_exp_coords())
    xp_assert_close(tf0.as_matrix(), tf1.as_matrix(), atol=atol)

    tf1 = RigidTransform.from_matrix(tf0.as_matrix())
    xp_assert_close(tf0.as_matrix(), tf1.as_matrix(), atol=atol)

    tf1 = RigidTransform.from_dual_quat(tf0.as_dual_quat())
    xp_assert_close(tf0.as_matrix(), tf1.as_matrix(), atol=atol)

    # exp_coords small rotation
    t = xp.asarray(rng.normal(scale=1000.0, size=shape + (3,)), dtype=dtype)
    rotvec = xp.asarray(rng.normal(scale=1e-10, size=shape + (3,)), dtype=dtype)
    r = Rotation.from_rotvec(rotvec)
    tf0 = RigidTransform.from_components(t, r)
    tf1 = RigidTransform.from_exp_coords(tf0.as_exp_coords())
    xp_assert_close(tf0.as_matrix(), tf1.as_matrix(), atol=atol)

