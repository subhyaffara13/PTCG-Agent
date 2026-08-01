
def eval_evec(symmetric, d, typ, k, which, v0=None, sigma=None,
              mattype=np.asarray, OPpart=None, mode='normal', rng=None):
    general = ('bmat' in d)

    if symmetric:
        eigs_func = eigsh
    else:
        eigs_func = eigs

    if general:
        err = (f"error for {eigs_func.__name__}:general, typ={typ}, which={which}, "
               f"sigma={sigma}, mattype={mattype.__name__},"
               f" OPpart={OPpart}, mode={mode}")
    else:
        err = (f"error for {eigs_func.__name__}:standard, typ={typ}, which={which}, "
               f"sigma={sigma}, mattype={mattype.__name__}, "
               f"OPpart={OPpart}, mode={mode}")

    a = d['mat'].astype(typ)
    ac = mattype(a)

    if general:
        b = d['bmat'].astype(typ)
        bc = mattype(b)

    # get exact eigenvalues
    exact_eval = d['eval'].astype(typ.upper())
    ind = argsort_which(exact_eval, typ, k, which,
                        sigma, OPpart, mode)
    exact_eval = exact_eval[ind]

    # compute arpack eigenvalues
    kwargs = dict(which=which, v0=v0, sigma=sigma, rng=rng)
    if eigs_func is eigsh:
        kwargs['mode'] = mode
    else:
        kwargs['OPpart'] = OPpart

    # compute suitable tolerances
    kwargs['tol'], rtol, atol = _get_test_tolerance(typ, mattype, d, which)
    # on rare occasions, ARPACK routines return results that are proper
    # eigenvalues and -vectors, but not necessarily the ones requested in
    # the parameter which. This is inherent to the Krylov methods, and
    # should not be treated as a failure. If such a rare situation
    # occurs, the calculation is tried again (but at most a few times).
    ntries = 0
    while ntries < 5:
        # solve
        if general:
            try:
                eigenvalues, evec = eigs_func(ac, k, bc, **kwargs)
            except ArpackNoConvergence:
                kwargs['maxiter'] = 20*a.shape[0]
                eigenvalues, evec = eigs_func(ac, k, bc, **kwargs)
        else:
            try:
                eigenvalues, evec = eigs_func(ac, k, **kwargs)
            except ArpackNoConvergence:
                kwargs['maxiter'] = 20*a.shape[0]
                eigenvalues, evec = eigs_func(ac, k, **kwargs)

        ind = argsort_which(eigenvalues, typ, k, which,
                            sigma, OPpart, mode)
        eigenvalues = eigenvalues[ind]
        evec = evec[:, ind]

        try:
            # check eigenvalues
            assert_allclose_cc(eigenvalues, exact_eval, rtol=rtol, atol=atol,
                               err_msg=err)
            check_evecs = True
        except AssertionError:
            check_evecs = False
            ntries += 1

        if check_evecs:
            # check eigenvectors
            LHS = np.dot(a, evec)
            if general:
                RHS = eigenvalues * np.dot(b, evec)
            else:
                RHS = eigenvalues * evec

            assert_allclose(LHS, RHS, rtol=rtol, atol=atol, err_msg=err)
            break

    # check eigenvalues
    assert_allclose_cc(eigenvalues, exact_eval, rtol=rtol, atol=atol, err_msg=err)

