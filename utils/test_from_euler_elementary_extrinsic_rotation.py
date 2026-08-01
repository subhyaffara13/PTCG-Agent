
def test_from_euler_elementary_extrinsic_rotation(xp):
    atol = 1e-12
    # Simple test to check if extrinsic rotations are implemented correctly
    mat = Rotation.from_euler('zx', xp.asarray([90, 90]), degrees=True).as_matrix()
    expected_mat = xp.asarray([
        [0.0, -1, 0],
        [0, 0, -1],
        [1, 0, 0]
    ])
    xp_assert_close(mat, expected_mat, atol=atol)

