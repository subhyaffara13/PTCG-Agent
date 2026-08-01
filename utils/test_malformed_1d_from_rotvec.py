
def test_malformed_1d_from_rotvec(xp):
    with pytest.raises(ValueError, match='Expected `rot_vec` to have shape'):
        Rotation.from_rotvec(xp.asarray([1, 2]))

