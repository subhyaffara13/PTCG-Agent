
def test_from_euler_input_validation(xp):
    # Single sequence with multiple angles
    with pytest.raises(ValueError, match="Expected last dimension of `angles` to"):
        Rotation.from_euler("X", xp.asarray([0, 90]))
    # Multiple sequences with single angle
    with pytest.raises(ValueError, match="Expected last dimension of `angles` to"):
        Rotation.from_euler("XYZ", xp.asarray([90]))

