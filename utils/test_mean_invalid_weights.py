
def test_mean_invalid_weights(xp):
    tf = RigidTransform.from_matrix(xp.tile(xp.eye(4), (4, 1, 1)))
    if is_lazy_array(tf.as_matrix()):
        m = tf.mean(weights=-xp.ones(4))
        assert xp.all(xp.isnan(m.as_matrix()))
    else:
        with pytest.raises(ValueError, match="non-negative"):
            tf.mean(weights=-xp.ones(4))

    # Test weight shape mismatch
    tf = RigidTransform.from_matrix(xp.eye(4))
    with pytest.raises(ValueError, match="Expected `weights` to"):
        tf.mean(weights=xp.ones((2,)))
    tf = RigidTransform.from_matrix(xp.tile(xp.eye(4), (3, 2, 1, 1, 1)))
    with pytest.raises(ValueError, match="Expected `weights` to"):
        tf.mean(weights=xp.ones((2, 1)))

