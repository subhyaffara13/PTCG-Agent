
def test_align_vectors_parallel(xp):
    atol = 1e-12
    a = xp.asarray([[1.0, 0, 0], [0, 1, 0]])
    b = xp.asarray([[0.0, 1, 0], [0, 1, 0]])
    m_expected = xp.asarray([[0.0, 1, 0],
                             [-1, 0, 0],
                             [0, 0, 1]])
    R, _ = Rotation.align_vectors(a, b, weights=[xp.inf, 1])
    xp_assert_close(R.as_matrix(), m_expected, atol=atol)
    R, _ = Rotation.align_vectors(a[0, ...], b[0, ...])
    xp_assert_close(R.as_matrix(), m_expected, atol=atol)
    xp_assert_close(R.apply(b[0, ...]), a[0, ...], atol=atol)

    b = xp.asarray([[1, 0, 0], [1, 0, 0]])
    m_expected = xp.asarray([[1.0, 0, 0],
                             [0, 1, 0],
                             [0, 0, 1]])
    R, _ = Rotation.align_vectors(a, b, weights=[xp.inf, 1])
    xp_assert_close(R.as_matrix(), m_expected, atol=atol)
    R, _ = Rotation.align_vectors(a[0, ...], b[0, ...])
    xp_assert_close(R.as_matrix(), m_expected, atol=atol)
    xp_assert_close(R.apply(b[0, ...]), a[0, ...], atol=atol)

