
def test_slerp_single_rot(xp):
    r = Rotation.from_quat(xp.asarray([[1.0, 2, 3, 4]]))
    with pytest.raises(ValueError, match=SLERP_EXCEPTION_MESSAGE):
        Slerp([1], r)

