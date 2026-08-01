
def test_mean_axis(xp, ndim: int):
    axes = xp.tile(xp.concat((-xp.eye(3), xp.eye(3))), (3,) * (ndim - 1) + (1, 1))
    theta = xp.pi / 4
    r = Rotation.from_rotvec(theta * axes)
    tf = RigidTransform.from_rotation(r)

    # Test mean over last axis
    desired = xp.full(axes.shape[:-2], 0.0)
    if ndim == 1:
        desired = desired[()]
    atol = 1e-6 if xpx.default_dtype(xp) is xp.float32 else 1e-10
    xp_assert_close(tf.mean(axis=-1).rotation.magnitude(), desired, atol=atol)

    # Test tuple axes
    desired = xp.full(axes.shape[1:-2], 0.0)
    if ndim < 3:
        desired = desired[()]
    xp_assert_close(tf.mean(axis=(0, -1)).rotation.magnitude(), desired, atol=atol)

    # Empty axis tuple should return RigidTransform unchanged
    tf_mean = tf.mean(axis=())
    xp_assert_close(tf_mean.as_matrix(), tf.as_matrix(), atol=atol)


def test_mean_axis(xp, ndim: int):
    axes = xp.tile(xp.concat((-xp.eye(3), xp.eye(3))), (3,) * (ndim - 1) + (1, 1))
    theta = xp.pi / 4
    r = Rotation.from_rotvec(theta * axes)

    # Test mean over last axis
    desired = xp.full(axes.shape[:-2], 0.0)
    if ndim == 1:
        desired = desired[()]
    atol = 1e-6 if xp_default_dtype(xp) is xp.float32 else 1e-10
    xp_assert_close(r.mean(axis=-1).magnitude(), desired, atol=atol)

    # Test tuple axes
    desired = xp.full(axes.shape[1:-2], 0.0)
    if ndim < 3:
        desired = desired[()]
    xp_assert_close(r.mean(axis=(0, -1)).magnitude(), desired, atol=atol)

    # Empty axis tuple should return Rotation unchanged
    r_mean = r.mean(axis=())
    xp_assert_close(r_mean.as_quat(canonical=True), r.as_quat(canonical=True),
                    atol=atol)

