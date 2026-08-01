
def test_rotation_promotion(xp):
    """Test that Rotation is promoted to RigidTransform in composition."""
    atol = 1e-12
    dtype = xpx.default_dtype(xp)
    rng = np.random.default_rng(0)

    t = xp.asarray(rng.normal(size=(3,)), dtype=dtype)
    r1 = rotation_to_xp(Rotation.random(rng=rng), xp)
    r2 = rotation_to_xp(Rotation.random(rng=rng), xp)
    tf = RigidTransform.from_components(t, r2)

    # RigidTransform * Rotation
    result = tf * r1
    expected = tf * RigidTransform.from_rotation(r1)
    assert isinstance(result, RigidTransform)
    xp_assert_close(result.as_matrix(), expected.as_matrix(), atol=atol)

    # Rotation * RigidTransform
    result = r1 * tf
    expected = RigidTransform.from_rotation(r1) * tf
    assert isinstance(result, RigidTransform)
    xp_assert_close(result.as_matrix(), expected.as_matrix(), atol=atol)

