
def test_slerp_rot_is_rotation(xp):
    with pytest.raises(TypeError, match="must be a `Rotation` instance"):
        r = xp.asarray([[1,2,3,4],
                        [0,0,0,1]])
        t = xp.asarray([0, 1])
        Slerp(t, r)

