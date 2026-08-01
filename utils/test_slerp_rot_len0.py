
def test_slerp_rot_len0(xp):
    r = Rotation.random()
    r = Rotation.from_quat(xp.asarray(r.as_quat()))
    with pytest.raises(ValueError, match=SLERP_EXCEPTION_MESSAGE):
        Slerp([], r)

