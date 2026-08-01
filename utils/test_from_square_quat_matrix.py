
def test_from_square_quat_matrix(xp):
    # Ensure proper norm array broadcasting
    x = xp.asarray([
        [3.0, 0, 0, 4],
        [5, 0, 12, 0],
        [0, 0, 0, 1],
        [-1, -1, -1, 1],
        [0, 0, 0, -1],  # Check double cover
        [-1, -1, -1, -1]  # Check double cover
        ])
    r = Rotation.from_quat(x)
    expected_quat = x / xp.asarray([[5.0], [13], [1], [2], [1], [2]])
    xp_assert_close(r.as_quat(), expected_quat)

