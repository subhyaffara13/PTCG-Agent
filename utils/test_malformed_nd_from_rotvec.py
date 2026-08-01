
def test_malformed_nd_from_rotvec(xp, ndim: int):
    shape = (1,) * (ndim - 1) + (2,)
    with pytest.raises(ValueError, match='Expected `rot_vec` to have shape'):
        Rotation.from_rotvec(xp.ones(shape))

