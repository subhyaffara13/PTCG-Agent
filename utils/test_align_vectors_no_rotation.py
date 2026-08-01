
def test_align_vectors_no_rotation(xp):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-5
    x = xp.asarray([[1, 2, 3], [4, 5, 6]], dtype=dtype)
    y = xp.asarray(x, copy=True)

    r, rssd = Rotation.align_vectors(x, y)
    xp_assert_close(r.as_matrix(), xp.eye(3), atol=atol)
    xp_assert_close(rssd, xp.asarray(0.0)[()], check_shape=False, atol=1e-6)

