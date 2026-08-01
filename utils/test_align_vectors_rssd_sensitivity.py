
def test_align_vectors_rssd_sensitivity(xp):
    rssd_expected = xp.asarray(0.141421356237308)[()]
    sens_expected = xp.asarray([[0.2, 0. , 0.],
                                [0. , 1.5, 1.],
                                [0. , 1. , 1.]])
    atol = 1e-6
    a = xp.asarray([[0, 1, 0], [0, 1, 1], [0, 1, 1]])
    b = xp.asarray([[1, 0, 0], [1, 1.1, 0], [1, 0.9, 0]])
    rot, rssd, sens = Rotation.align_vectors(a, b, return_sensitivity=True)
    xp_assert_close(rssd, rssd_expected, atol=atol)
    xp_assert_close(sens, sens_expected, atol=atol)

