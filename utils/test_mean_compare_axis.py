
def test_mean_compare_axis(xp):
    # Create a random set of transforms and compare the mean over an axis with
    # the mean without axis of the sliced transform
    atol = 1e-10 if xpx.default_dtype(xp) == xp.float64 else 1e-6
    rng = np.random.default_rng(0)
    q = xp.asarray(rng.normal(size=(4, 5, 6, 4)), dtype=xpx.default_dtype(xp))
    r = Rotation.from_quat(q)
    t = xp.asarray(rng.normal(size=(4, 5, 6, 3)), dtype=xpx.default_dtype(xp))
    tf = RigidTransform.from_components(t, r)

    mean_0 = tf.mean(axis=0)
    for i in range(q.shape[1]):
        for j in range(q.shape[2]):
            r_slice = Rotation.from_quat(q[:, i, j, ...])
            t_slice = t[:, i, j, ...]
            mean_slice_tf = RigidTransform.from_components(t_slice, r_slice).mean()
            xp_assert_close(
                (mean_0[i][j].rotation * mean_slice_tf.rotation.inv()).magnitude(),
                xp.asarray(0.0)[()], atol=atol,
            )
            xp_assert_close(
                mean_0[i][j].translation, mean_slice_tf.translation, atol=atol,
            )
    mean_1_2 = tf.mean(axis=(1, 2))
    for i in range(q.shape[0]):
        r_slice = Rotation.from_quat(q[i, ...])
        t_slice = t[i, ...]
        mean_slice_tf = RigidTransform.from_components(t_slice, r_slice).mean()
        xp_assert_close(
            (mean_1_2[i].rotation * mean_slice_tf.rotation.inv()).magnitude(),
            xp.asarray(0.0)[()], atol=atol,
        )
        xp_assert_close(
            mean_1_2[i].translation, mean_slice_tf.translation, atol=atol,
        )


def test_mean_compare_axis(xp):
    # Create a random set of rotations and compare the mean over an axis with the
    # mean without axis of the sliced quaternion
    atol = 1e-10 if xpx.default_dtype(xp) == xp.float64 else 1e-6
    rng = np.random.default_rng(0)
    q = xp.asarray(rng.normal(size=(4, 5, 6, 4)), dtype=xpx.default_dtype(xp))
    r = Rotation.from_quat(q)

    mean_0 = r.mean(axis=0)
    for i in range(q.shape[1]):
        for j in range(q.shape[2]):
            mean_slice = Rotation.from_quat(q[:, i, j, ...]).mean()
            xp_assert_close((mean_0[i][j] * mean_slice.inv()).magnitude(),
                            xp.asarray(0.0)[()], atol=atol)
    mean_1_2 = r.mean(axis=(1, 2))
    for i in range(q.shape[0]):
        mean_slice = Rotation.from_quat(q[i, ...]).mean()
        xp_assert_close((mean_1_2[i] * mean_slice.inv()).magnitude(),
                        xp.asarray(0.0)[()], atol=atol)

