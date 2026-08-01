
def test_from_rotvec_int_dtype(xp):
    rotvec = xp.asarray([1, 0, 0])
    r = Rotation.from_rotvec(rotvec)
    assert r.as_quat().dtype == xp_default_dtype(xp)

