
def _get_solver(M, sparse=False, lstsq=False, sym_pos=True,
                cholesky=True, permc_spec='MMD_AT_PLUS_A'):
    """
    Given solver options, return a handle to the appropriate linear system
    solver.

    Parameters
    ----------
    M : 2-D array
        As defined in [4] Equation 8.31
    sparse : bool (default = False)
        True if the system to be solved is sparse. This is typically set
        True when the original ``A_ub`` and ``A_eq`` arrays are sparse.
    lstsq : bool (default = False)
        True if the system is ill-conditioned and/or (nearly) singular and
        thus a more robust least-squares solver is desired. This is sometimes
        needed as the solution is approached.
    sym_pos : bool (default = True)
        True if the system matrix is symmetric positive definite
        Sometimes this needs to be set false as the solution is approached,
        even when the system should be symmetric positive definite, due to
        numerical difficulties.
    cholesky : bool (default = True)
        True if the system is to be solved by Cholesky, rather than LU,
        decomposition. This is typically faster unless the problem is very
        small or prone to numerical difficulties.
    permc_spec : str (default = 'MMD_AT_PLUS_A')
        Sparsity preservation strategy used by SuperLU. Acceptable values are:

        - ``NATURAL``: natural ordering.
        - ``MMD_ATA``: minimum degree ordering on the structure of A^T A.
        - ``MMD_AT_PLUS_A``: minimum degree ordering on the structure of A^T+A.
        - ``COLAMD``: approximate minimum degree column ordering.

        See SuperLU documentation.

    Returns
    -------
    solve : function
        Handle to the appropriate solver function

    """
    try:
        if sparse:
            if lstsq:
                def solve(r, sym_pos=False):
                    return sps.linalg.lsqr(M, r)[0]
            elif cholesky:
                # TODO: revert this suppress_warning once the warning bug fix in
                # sksparse is merged/released
                # Suppress spurious warning bug from sksparse with csc_array gh-22089
                # try:
                #     # Will raise an exception in the first call,
                #     # or when the matrix changes due to a new problem
                #     _get_solver.cholmod_factor.cholesky_inplace(M)
                # except Exception:
                #     _get_solver.cholmod_factor = cholmod_analyze(M)
                #     _get_solver.cholmod_factor.cholesky_inplace(M)
                with catch_warnings(
                    action='ignore', category=CholmodTypeConversionWarning
                ):
                    try:
                        # Will raise an exception in the first call,
                        # or when the matrix changes due to a new problem
                        _get_solver.cholmod_factor.cholesky_inplace(M)
                    except Exception:
                        _get_solver.cholmod_factor = cholmod_analyze(M)
                        _get_solver.cholmod_factor.cholesky_inplace(M)
                solve = _get_solver.cholmod_factor
            else:
                if has_umfpack and sym_pos:
                    solve = sps.linalg.factorized(M)
                else:  # factorized doesn't pass permc_spec
                    solve = sps.linalg.splu(M, permc_spec=permc_spec).solve

        else:
            if lstsq:  # sometimes necessary as solution is approached
                def solve(r):
                    return sp.linalg.lstsq(M, r)[0]
            elif cholesky:
                L = sp.linalg.cho_factor(M)

                def solve(r):
                    return sp.linalg.cho_solve(L, r)
            else:
                # this seems to cache the matrix factorization, so solving
                # with multiple right hand sides is much faster
                def solve(r, sym_pos=sym_pos):
                    if sym_pos:
                        return sp.linalg.solve(M, r, assume_a="pos")
                    else:
                        return sp.linalg.solve(M, r)
    # There are many things that can go wrong here, and it's hard to say
    # what all of them are. It doesn't really matter: if the matrix can't be
    # factorized, return None. get_solver will be called again with different
    # inputs, and a new routine will try to factorize the matrix.
    except KeyboardInterrupt:
        raise
    except Exception:
        return None
    return solve

