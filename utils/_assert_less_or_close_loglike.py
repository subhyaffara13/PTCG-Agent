
def _assert_less_or_close_loglike(dist, data, func=None, maybe_identical=False,
                                  **kwds):
    """
    This utility function checks that the negative log-likelihood function
    (or `func`) of the result computed using dist.fit() is less than or equal
    to the result computed using the generic fit method.  Because of
    normal numerical imprecision, the "equality" check is made using
    `np.allclose` with a relative tolerance of 1e-15.
    """
    if func is None:
        func = dist.nnlf

    mle_analytical = dist.fit(data, **kwds)
    numerical_opt = super(type(dist), dist).fit(data, **kwds)

    # Sanity check that the analytical MLE is actually executed.
    # Due to floating point arithmetic, the generic MLE is unlikely
    # to produce the exact same result as the analytical MLE.
    if not maybe_identical:
        assert np.any(mle_analytical != numerical_opt)

    ll_mle_analytical = func(mle_analytical, data)
    ll_numerical_opt = func(numerical_opt, data)
    assert (ll_mle_analytical <= ll_numerical_opt or
            np.allclose(ll_mle_analytical, ll_numerical_opt, rtol=1e-15))

    # Ideally we'd check that shapes are correctly fixed, too, but that is
    # complicated by the many ways of fixing them (e.g. f0, fix_a, fa).
    if 'floc' in kwds:
        assert mle_analytical[-2] == kwds['floc']
    if 'fscale' in kwds:
        assert mle_analytical[-1] == kwds['fscale']

