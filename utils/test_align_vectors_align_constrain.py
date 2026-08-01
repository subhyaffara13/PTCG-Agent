
def test_align_vectors_align_constrain(xp):
    # Align the primary +X B axis with the primary +Y A axis, and rotate about
    # it such that the +Y B axis (residual of the [1, 1, 0] secondary b vector)
    # is aligned with the +Z A axis (residual of the [0, 1, 1] secondary a
    # vector)
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-6
    b = xp.asarray([[1, 0, 0], [1, 1, 0]])
    a = xp.asarray([[0.0, 1, 0], [0, 1, 1]])
    m_expected = xp.asarray([[0.0, 0, 1],
                             [1, 0, 0],
                             [0, 1, 0]])
    R, rssd = Rotation.align_vectors(a, b, weights=xp.asarray([xp.inf, 1]))
    xp_assert_close(R.as_matrix(), m_expected, atol=atol)
    xp_assert_close(R.apply(b), a, atol=atol)  # Pri and sec align exactly
    xp_assert_close(rssd, xp.asarray(0.0)[()], atol=atol)

    # Do the same but with an inexact secondary rotation
    b = xp.asarray([[1, 0, 0], [1, 2, 0]])
    rssd_expected = 1.0
    R, rssd = Rotation.align_vectors(a, b, weights=xp.asarray([xp.inf, 1]))
    xp_assert_close(R.as_matrix(), m_expected, atol=atol)
    xp_assert_close(R.apply(b)[0, ...], a[0, ...], atol=atol)  # Only pri aligns exactly
    assert xpx.isclose(rssd, rssd_expected, atol=atol, xp=xp)
    a_expected = xp.asarray([[0.0, 1, 0], [0, 1, 2]])
    xp_assert_close(R.apply(b), a_expected, atol=atol)

    # Check random vectors
    b = xp.asarray([[1, 2, 3], [-2, 3, -1]])
    a = xp.asarray([[-1.0, 3, 2], [1, -1, 2]])
    rssd_expected = 1.3101595297515016
    R, rssd = Rotation.align_vectors(a, b, weights=xp.asarray([xp.inf, 1]))
    xp_assert_close(R.apply(b)[0, ...], a[0, ...], atol=atol)  # Only pri aligns exactly
    assert xpx.isclose(rssd, rssd_expected, atol=atol, xp=xp)

