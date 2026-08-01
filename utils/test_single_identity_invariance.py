
def test_single_identity_invariance(xp):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-7
    n = 10
    p = rotation_to_xp(Rotation.random(n, rng=0), xp)
    q = rotation_to_xp(Rotation.identity(), xp)
    result = p * q
    xp_assert_close(p.as_quat(), result.as_quat())

    result = result * p.inv()
    xp_assert_close(result.magnitude(), xp.zeros(n), atol=atol)

