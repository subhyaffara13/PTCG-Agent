
def test_align_vectors_improper_rotation(xp):
    dtype = xpx.default_dtype(xp)
    atol = 1e-7 if dtype == xp.float64 else 1e-3
    # Tests correct logic for issue #10444
    x = xp.asarray([[0.89299824, -0.44372674, 0.0752378],
                    [0.60221789, -0.47564102, -0.6411702]])
    y = xp.asarray([[0.02386536, -0.82176463, 0.5693271],
                    [-0.27654929, -0.95191427, -0.1318321]])

    est, rssd = Rotation.align_vectors(x, y)
    xp_assert_close(x, est.apply(y), atol=1e-6)
    xp_assert_close(rssd, xp.asarray(0.0)[()], check_shape=False, atol=atol)

