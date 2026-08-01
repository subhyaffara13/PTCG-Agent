
def test_from_matrix_calculation(xp):
    atol = 1e-8
    expected_quat = xp.asarray([1.0, 1, 6, 1]) / math.sqrt(39)
    mat = xp.asarray([
            [-0.8974359, -0.2564103, 0.3589744],
            [0.3589744, -0.8974359, 0.2564103],
            [0.2564103, 0.3589744, 0.8974359]
            ])
    xp_assert_close(Rotation.from_matrix(mat).as_quat(), expected_quat, atol=atol)
    xp_assert_close(Rotation.from_matrix(xp.reshape(mat, (1, 3, 3))).as_quat(),
                    xp.reshape(expected_quat, (1, 4)),
                    atol=atol)

