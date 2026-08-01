
def test_multiplication_stability(xp):
    qs = rotation_to_xp(Rotation.random(50, rng=0), xp)
    rs = rotation_to_xp(Rotation.random(1000, rng=1), xp)
    expected = xp.ones(len(rs))
    for r in qs:
        rs = rs * r * rs
        xp_assert_close(xp_vector_norm(rs.as_quat(), axis=1), expected)

