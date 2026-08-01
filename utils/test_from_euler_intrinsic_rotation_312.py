
def test_from_euler_intrinsic_rotation_312(xp):
    atol = 1e-7
    angles = xp.asarray([
        [30, 60, 45],
        [30, 60, 30],
        [45, 30, 60]
        ])
    mat = Rotation.from_euler('ZXY', angles, degrees=True).as_matrix()

    xp_assert_close(mat[0, ...], xp.asarray([
        [0.3061862, -0.2500000, 0.9185587],
        [0.8838835, 0.4330127, -0.1767767],
        [-0.3535534, 0.8660254, 0.3535534]
    ]), atol=atol)

    xp_assert_close(mat[1, ...], xp.asarray([
        [0.5334936, -0.2500000, 0.8080127],
        [0.8080127, 0.4330127, -0.3995191],
        [-0.2500000, 0.8660254, 0.4330127]
    ]), atol=atol)

    xp_assert_close(mat[2, ...], xp.asarray([
        [0.0473672, -0.6123725, 0.7891491],
        [0.6597396, 0.6123725, 0.4355958],
        [-0.7500000, 0.5000000, 0.4330127]
    ]), atol=atol)

