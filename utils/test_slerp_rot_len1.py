
def test_slerp_rot_len1(xp):
    r = Rotation.random(1)
    r = Rotation.from_quat(xp.asarray(r.as_quat()))
    with pytest.raises(ValueError, match=SLERP_EXCEPTION_MESSAGE):
        Slerp([1], r)

