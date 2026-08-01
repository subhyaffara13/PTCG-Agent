
def test_from_mrp_int_dtype(xp):
    mrp = xp.asarray([0, 0, 1])
    r = Rotation.from_mrp(mrp)
    assert r.as_quat().dtype == xp_default_dtype(xp)

