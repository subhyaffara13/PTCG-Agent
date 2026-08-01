
def test_concatenate_wrong_shape(xp):
    r1 = Rotation.from_quat(xp.ones((5, 2, 4)))
    r2 = Rotation.from_quat(xp.ones((1, 4)))
    # Frameworks throw inconsistent error types on concat failures
    with pytest.raises((ValueError, RuntimeError, TypeError)):
        Rotation.concatenate([r1, r2])

