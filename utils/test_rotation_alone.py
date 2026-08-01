
def test_rotation_alone(xp):
    atol = 1e-12

    r = Rotation.from_euler('z', xp.asarray(90), degrees=True)
    tf = RigidTransform.from_rotation(r)
    vec = xp.asarray([1, 0, 0])
    expected = r.apply(vec)
    xp_assert_close(tf.apply(vec), expected, atol=atol)

