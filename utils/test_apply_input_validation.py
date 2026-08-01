
def test_apply_input_validation(xp):
    r = Rotation.from_quat(xp.ones(4))
    with pytest.raises(ValueError, match="Expected input of shape"):
        r.apply(xp.ones(2))
    with pytest.raises(ValueError, match="Expected input of shape"):
        r.apply(xp.ones((2, 2)))
    r = Rotation.from_quat(xp.ones((2, 4)))
    with pytest.raises(ValueError, match="Cannot broadcast"):
        r.apply(xp.ones((3, 3)))
    r = Rotation.from_quat(xp.ones((1, 7, 2, 4)))
    with pytest.raises(ValueError, match="Cannot broadcast"):
        r.apply(xp.ones((2, 2, 3)))

