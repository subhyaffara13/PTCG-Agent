
def test_from_quat_int_dtype(xp):
    r = Rotation.from_quat(xp.asarray([1, 0, 0, 0]))
    assert r.as_quat().dtype == xp_default_dtype(xp)

