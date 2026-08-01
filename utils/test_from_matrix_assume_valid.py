
def test_from_matrix_assume_valid(xp):
    rng = np.random.default_rng(0)
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-6
    # Test that normal matrices remain unchanged
    rot = rotation_to_xp(Rotation.from_quat(rng.normal(size=(10, 4))), xp)
    rot_no_norm = Rotation.from_matrix(rot.as_matrix(), assume_valid=True)
    assert xp.all(rot.approx_equal(rot_no_norm, atol=atol))

