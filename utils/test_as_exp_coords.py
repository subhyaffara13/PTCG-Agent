
def test_as_exp_coords(xp, ndim: int):
    shape = (ndim,) * (ndim - 1)
    # identity
    expected = xp.zeros(shape + (6,))
    actual = RigidTransform.from_exp_coords(expected).as_exp_coords()
    xp_assert_close(actual, expected, atol=1e-12)

    rng = np.random.default_rng(10)

    # pure rotation
    rot_vec = xp.asarray(rng.normal(scale=0.1, size=shape + (1000, 3)))
    tf = RigidTransform.from_rotation(Rotation.from_rotvec(rot_vec))
    exp_coords = tf.as_exp_coords()
    xp_assert_close(exp_coords[..., :3], rot_vec, atol=1e-12)
    expected = xp.zeros_like(rot_vec)
    xp_assert_close(exp_coords[..., 3:], expected, atol=1e-16)

    # pure translation
    translation = xp.asarray(rng.normal(scale=100.0, size=shape + (1000, 3)))
    tf = RigidTransform.from_translation(translation)
    exp_coords = tf.as_exp_coords()
    xp_assert_close(exp_coords[..., :3], expected, atol=1e-16)
    xp_assert_close(exp_coords[..., 3:], translation, atol=1e-15)

