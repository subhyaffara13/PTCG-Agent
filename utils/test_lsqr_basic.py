
def test_lsqr_basic():
    b_copy = b.copy()
    xo, *_ = lsqr(G, b, show=show, atol=tol, btol=tol, iter_lim=maxit)
    assert_array_equal(b_copy, b)

    svx = np.linalg.solve(G, b)
    assert_allclose(xo, svx, atol=atol_test, rtol=rtol_test)

    # Now the same but with damp > 0.
    # This is equivalent to solving the extended system:
    # ( G      ) @ x = ( b )
    # ( damp*I )       ( 0 )
    damp = 1.5
    xo, *_ = lsqr(
        G, b, damp=damp, show=show, atol=tol, btol=tol, iter_lim=maxit)

    Gext = np.r_[G, damp * np.eye(G.shape[1])]
    bext = np.r_[b, np.zeros(G.shape[1])]
    svx, *_ = np.linalg.lstsq(Gext, bext, rcond=None)
    assert_allclose(xo, svx, atol=atol_test, rtol=rtol_test)

