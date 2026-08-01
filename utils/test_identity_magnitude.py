
def test_identity_magnitude(xp):
    n = 10
    r = rotation_to_xp(Rotation.identity(n), xp)
    expected = xp.zeros(n)
    xp_assert_close(r.magnitude(), expected)
    xp_assert_close(r.inv().magnitude(), expected)

