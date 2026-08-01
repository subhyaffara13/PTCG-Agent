
def test_translation_alone(xp):
    atol = 1e-12
    t = xp.asarray([1.0, 2, 3])
    tf = RigidTransform.from_translation(t)
    vec = xp.asarray([5.0, 6, 7])
    expected = t + vec
    xp_assert_close(tf.apply(vec), expected, atol=atol)

