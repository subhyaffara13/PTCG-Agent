
def test_quat_double_to_canonical_single_cover(xp):
    x = xp.asarray([
        [-1.0, 0, 0, 0],
        [0, -1, 0, 0],
        [0, 0, -1, 0],
        [0, 0, 0, -1],
        [-1, -1, -1, -1]
        ])
    r = Rotation.from_quat(x)
    expected_quat = xp.abs(x) / xp_vector_norm(x, axis=1)[:, None]
    xp_assert_close(r.as_quat(canonical=True), expected_quat)

