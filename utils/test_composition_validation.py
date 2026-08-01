
def test_composition_validation(xp):
    tf2 = RigidTransform.from_translation(xp.asarray([[1, 2, 3], [4, 5, 6]]))
    tf3 = RigidTransform.from_translation(xp.asarray([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

    # Test incompatible shapes
    with pytest.raises(ValueError, match="Cannot broadcast"):
        tf2 * tf3

    tf4 = RigidTransform.from_matrix(xp.tile(xp.eye(4), (1, 4, 1, 1)))
    # Test invalid broadcasting shape
    with pytest.raises(ValueError, match="Cannot broadcast"):
        tf2 * tf4

