
def test_quat_canonical(xp):
    # Case 0: w < 0
    q = xp.asarray([0.0, 0, 0, -1])
    xp_assert_close(Rotation.from_quat(q).as_quat(canonical=True), -q)
    # Case 1: w == 0, x < 0
    q = xp.asarray([-1.0, 0, 0, 0])
    xp_assert_close(Rotation.from_quat(q).as_quat(canonical=True), -q)
    # Case 2: w == 0, x == 0, y < 0
    q = xp.asarray([0.0, -1, 0, 0])
    xp_assert_close(Rotation.from_quat(q).as_quat(canonical=True), -q)
    # Case 3: w == 0, x == 0, y == 0, z < 0
    q = xp.asarray([0.0, 0, -1, 0])
    xp_assert_close(Rotation.from_quat(q).as_quat(canonical=True), -q)
    # Other cases: w > 0, y < 0
    q = xp.asarray([0.0, -0.1, 0, 0.9])
    q = q / xp_vector_norm(q)
    xp_assert_close(Rotation.from_quat(q).as_quat(canonical=True), q)
    # Other cases: w > 0, z < 0
    q = xp.asarray([0.0, 0.0, -0.1, 0.9])
    q = q / xp_vector_norm(q)
    xp_assert_close(Rotation.from_quat(q).as_quat(canonical=True), q)

