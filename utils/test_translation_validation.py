
def test_translation_validation(xp):
    # Test invalid translation shapes
    with pytest.raises(ValueError, match="Expected `translation` to have shape"):
        RigidTransform.from_translation(xp.asarray([1, 2]))

    with pytest.raises(ValueError, match="Expected `translation` to have shape"):
        RigidTransform.from_translation(xp.zeros((2, 2)))

