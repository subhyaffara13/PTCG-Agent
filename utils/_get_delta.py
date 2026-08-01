
def _get_delta(A, b, c, x, y, z, tau, kappa, gamma, eta, sparse=False,
               lstsq=False, sym_pos=True, cholesky=True, pc=True, ip=False,
               permc_spec='MMD_AT_PLUS_A'):
    """
    Given standard form problem defined by ``A``, ``b``, and ``c``;
    current variable estimates ``x``, ``y``, ``z``, ``tau``, and ``kappa``;
    algorithmic parameters ``gamma and ``eta;
    and options ``sparse``, ``lstsq``, ``sym_pos``, ``cholesky``, ``pc``
    (predictor-corrector), and ``ip`` (initial point improvement),
    get the search direction for increments to the variable estimates.

    Parameters
    ----------
    As defined in [4], except:
    sparse : bool
        True if the system to be solved is sparse. This is typically set
        True when the original ``A_ub`` and ``A_eq`` arrays are sparse.
    lstsq : bool
        True if the system is ill-conditioned and/or (nearly) singular and
        thus a more robust least-squares solver is desired. This is sometimes
        needed as the solution is approached.
    sym_pos : bool
        True if the system matrix is symmetric positive definite
        Sometimes this needs to be set false as the solution is approached,
        even when the system should be symmetric positive definite, due to
        numerical difficulties.
    cholesky : bool
        True if the system is to be solved by Cholesky, rather than LU,
        decomposition. This is typically faster unless the problem is very
        small or prone to numerical difficulties.
    pc : bool
        True if the predictor-corrector method of Mehrota is to be used. This
        is almost always (if not always) beneficial. Even though it requires
        the solution of an additional linear system, the factorization
        is typically (implicitly) reused so solution is efficient, and the
        number of algorithm iterations is typically reduced.
    ip : bool
        True if the improved initial point suggestion due to [4] section 4.3
        is desired. It's unclear whether this is beneficial.
    permc_spec : str (default = 'MMD_AT_PLUS_A')
        (Has effect only with ``sparse = True``, ``lstsq = False``, ``sym_pos =
        True``.) A matrix is factorized in each iteration of the algorithm.
        This option specifies how to permute the columns of the matrix for
        sparsity preservation. Acceptable values are:

        - ``NATURAL``: natural ordering.
        - ``MMD_ATA``: minimum degree ordering on the structure of A^T A.
        - ``MMD_AT_PLUS_A``: minimum degree ordering on the structure of A^T+A.
        - ``COLAMD``: approximate minimum degree column ordering.

        This option can impact the convergence of the
        interior point algorithm; test different values to determine which
        performs best for your problem. For more information, refer to
        ``scipy.sparse.linalg.splu``.

    Returns
    -------
    Search directions as defined in [4]

    References
    ----------
    .. [4] Andersen, Erling D., and Knud D. Andersen. "The MOSEK interior point
           optimizer for linear programming: an implementation of the
           homogeneous algorithm." High performance optimization. Springer US,
           2000. 197-232.

    """
    if A.shape[0] == 0:
        # If there are no constraints, some solvers fail (understandably)
        # rather than returning empty solution. This gets the job done.
        lstsq, sym_pos, cholesky = False, True, False
    n_x = len(x)

    # [4] Equation 8.8
    r_P = b * tau - A.dot(x)
    r_D = c * tau - A.T.dot(y) - z
    r_G = c.dot(x) - b.transpose().dot(y) + kappa
    mu = (x.dot(z) + tau * kappa) / (n_x + 1)

    #  Assemble M from [4] Equation 8.31
    Dinv = x / z

    if sparse:
        M = A.dot(sps.diags_array(Dinv, format="csc").dot(A.T))
    else:
        M = A.dot(Dinv.reshape(-1, 1) * A.T)
    solve = _get_solver(M, sparse, lstsq, sym_pos, cholesky, permc_spec)

    # pc: "predictor-corrector" [4] Section 4.1
    # In development this option could be turned off
    # but it always seems to improve performance substantially
    n_corrections = 1 if pc else 0

    i = 0
    alpha, d_x, d_z, d_tau, d_kappa = 0, 0, 0, 0, 0
    while i <= n_corrections:
        # Reference [4] Eq. 8.6
        rhatp = eta(gamma) * r_P
        rhatd = eta(gamma) * r_D
        rhatg = eta(gamma) * r_G

        # Reference [4] Eq. 8.7
        rhatxs = gamma * mu - x * z
        rhattk = gamma * mu - tau * kappa

        if i == 1:
            if ip:  # if the correction is to get "initial point"
                # Reference [4] Eq. 8.23
                rhatxs = ((1 - alpha) * gamma * mu -
                          x * z - alpha**2 * d_x * d_z)
                rhattk = ((1 - alpha) * gamma * mu -
                    tau * kappa -
                    alpha**2 * d_tau * d_kappa)
            else:  # if the correction is for "predictor-corrector"
                # Reference [4] Eq. 8.13
                rhatxs -= d_x * d_z
                rhattk -= d_tau * d_kappa

        # sometimes numerical difficulties arise as the solution is approached
        # this loop tries to solve the equations using a sequence of functions
        # for solve. For dense systems, the order is:
        # 1. scipy.linalg.cho_factor/scipy.linalg.cho_solve,
        # 2. scipy.linalg.solve w/ sym_pos = True,
        # 3. scipy.linalg.solve w/ sym_pos = False, and if all else fails
        # 4. scipy.linalg.lstsq
        # For sparse systems, the order is:
        # 1. sksparse.cholmod.cholesky (if available)
        # 2. scipy.sparse.linalg.factorized (if umfpack available)
        # 3. scipy.sparse.linalg.splu
        # 4. scipy.sparse.linalg.lsqr
        solved = False
        while not solved:
            try:
                # [4] Equation 8.28
                p, q = _sym_solve(Dinv, A, c, b, solve)
                # [4] Equation 8.29
                u, v = _sym_solve(Dinv, A, rhatd -
                                  (1 / x) * rhatxs, rhatp, solve)
                if np.any(np.isnan(p)) or np.any(np.isnan(q)):
                    raise LinAlgError
                solved = True
            except (LinAlgError, ValueError, TypeError) as e:
                # Usually this doesn't happen. If it does, it happens when
                # there are redundant constraints or when approaching the
                # solution. If so, change solver.
                if cholesky:
                    cholesky = False
                    warn(
                        "Solving system with option 'cholesky':True "
                        "failed. It is normal for this to happen "
                        "occasionally, especially as the solution is "
                        "approached. However, if you see this frequently, "
                        "consider setting option 'cholesky' to False.",
                        OptimizeWarning, stacklevel=5)
                elif sym_pos:
                    sym_pos = False
                    warn(
                        "Solving system with option 'sym_pos':True "
                        "failed. It is normal for this to happen "
                        "occasionally, especially as the solution is "
                        "approached. However, if you see this frequently, "
                        "consider setting option 'sym_pos' to False.",
                        OptimizeWarning, stacklevel=5)
                elif not lstsq:
                    lstsq = True
                    warn(
                        "Solving system with option 'sym_pos':False "
                        "failed. This may happen occasionally, "
                        "especially as the solution is "
                        "approached. However, if you see this frequently, "
                        "your problem may be numerically challenging. "
                        "If you cannot improve the formulation, consider "
                        "setting 'lstsq' to True. Consider also setting "
                        "`presolve` to True, if it is not already.",
                        OptimizeWarning, stacklevel=5)
                else:
                    raise e
                solve = _get_solver(M, sparse, lstsq, sym_pos,
                                    cholesky, permc_spec)
        # [4] Results after 8.29
        d_tau = ((rhatg + 1 / tau * rhattk - (-c.dot(u) + b.dot(v))) /
                 (1 / tau * kappa + (-c.dot(p) + b.dot(q))))
        d_x = u + p * d_tau
        d_y = v + q * d_tau

        # [4] Relations between  after 8.25 and 8.26
        d_z = (1 / x) * (rhatxs - z * d_x)
        d_kappa = 1 / tau * (rhattk - kappa * d_tau)

        # [4] 8.12 and "Let alpha be the maximal possible step..." before 8.23
        alpha = _get_step(x, d_x, z, d_z, tau, d_tau, kappa, d_kappa, 1)
        if ip:  # initial point - see [4] 4.4
            gamma = 10
        else:  # predictor-corrector, [4] definition after 8.12
            beta1 = 0.1  # [4] pg. 220 (Table 8.1)
            gamma = (1 - alpha)**2 * min(beta1, (1 - alpha))
        i += 1

    return d_x, d_y, d_z, d_tau, d_kappa

