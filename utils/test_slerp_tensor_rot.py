
def test_slerp_tensor_rot(xp):
    r = Rotation.from_quat(xp.ones((2, 2, 4)))
    with pytest.raises(ValueError, match="Rotations with more than 1 leading"):
        Slerp([1, 2], r)

