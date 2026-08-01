
def initxfc(calcfc, iprint, maxfun, constr0, amat, bvec, ctol, f0, ftarget, rhobeg, x0,
            xhist, fhist, chist, conhist, maxhist):
    '''
    This subroutine does the initialization concerning X, function values, and
    constraints.
    '''

    # Local variables
    solver = 'COBYLA'
    srname = "INITIALIZE"

    # Sizes
    num_constraints = np.size(constr0)
    m_lcon = np.size(bvec) if bvec is not None else 0
    m_nlcon = num_constraints - m_lcon
    num_vars = np.size(x0)

    # Preconditions
    if DEBUGGING:
        assert num_constraints >= 0, f'M >= 0 {srname}'
        assert num_vars >= 1, f'N >= 1 {srname}'
        assert abs(iprint) <= 3, f'IPRINT is 0, 1, -1, 2, -2, 3, or -3 {srname}'
        # assert conmat.shape == (num_constraints , num_vars + 1), f'CONMAT.shape = [M, N+1] {srname}'
        # assert cval.size == num_vars + 1, f'CVAL.size == N+1 {srname}'
        # assert maxchist * (maxchist - maxhist) == 0, f'CHIST.shape == 0 or MAXHIST {srname}'
        # assert conhist.shape[0] == num_constraints and maxconhist * (maxconhist - maxhist) == 0, 'CONHIST.shape[0] == num_constraints, SIZE(CONHIST, 2) == 0 or MAXHIST {srname)}'
        # assert maxfhist * (maxfhist - maxhist) == 0, f'FHIST.shape == 0 or MAXHIST {srname}'
        # assert xhist.shape[0] == num_vars and maxxhist * (maxxhist - maxhist) == 0, 'XHIST.shape[0] == N, SIZE(XHIST, 2) == 0 or MAXHIST {srname)}'
        assert all(np.isfinite(x0)), f'X0 is finite {srname}'
        assert rhobeg > 0, f'RHOBEG > 0 {srname}'

    #====================#
    # Calculation starts #
    #====================#

    # Initialize info to the default value. At return, a value different from this
    # value will indicate an abnormal return
    info = INFO_DEFAULT

    # Initialize the simplex. It will be revised during the initialization.
    sim = np.eye(num_vars, num_vars+1) * rhobeg
    sim[:, num_vars] = x0

    # Initialize the matrix simi. In most cases simi is overwritten, but not always.
    simi = np.eye(num_vars) / rhobeg

    # evaluated[j] = True iff the function/constraint of SIM[:, j] has been evaluated.
    evaluated = np.zeros(num_vars+1, dtype=bool)

    # Initialize fval
    fval = np.zeros(num_vars+1) + REALMAX
    cval = np.zeros(num_vars+1) + REALMAX
    conmat = np.zeros((num_constraints, num_vars+1)) + REALMAX


    for k in range(num_vars + 1):
        x = sim[:, num_vars].copy()
        # We will evaluate F corresponding to SIM(:, J).
        if k == 0:
            j = num_vars
            f = f0
            constr = constr0
        else:
            j = k - 1
            x[j] += rhobeg
            f, constr = evaluate(calcfc, x, m_nlcon, amat, bvec)
        cstrv = np.max(np.append(0, constr))

        # Print a message about the function/constraint evaluation according to IPRINT.
        fmsg(solver, 'Initialization', iprint, k, rhobeg, f, x, cstrv, constr)

        # Save X, F, CONSTR, CSTRV into the history.
        savehist(maxhist, x, xhist, f, fhist, cstrv, chist, constr, conhist)

        # Save F, CONSTR, and CSTRV to FVAL, CONMAT, and CVAL respectively.
        evaluated[j] = True
        fval[j] = f
        conmat[:, j] = constr
        cval[j] = cstrv

        # Check whether to exit.
        subinfo = checkbreak_con(maxfun, k, cstrv, ctol, f, ftarget, x)
        if subinfo != INFO_DEFAULT:
            info = subinfo
            break

        # Exchange the new vertex of the initial simplex with the optimal vertex if necessary.
        # This is the ONLY part that is essentially non-parallel.
        if j < num_vars and fval[j] < fval[num_vars]:
            fval[j], fval[num_vars] = fval[num_vars], fval[j]
            cval[j], cval[num_vars] = cval[num_vars], cval[j]
            conmat[:, [j, num_vars]] = conmat[:, [num_vars, j]]
            sim[:, num_vars] = x
            sim[j, :j+1] = -rhobeg  # SIM[:, :j+1] is lower triangular

    nf = np.count_nonzero(evaluated)

    if evaluated.all():
        # Initialize SIMI to the inverse of SIM[:, :num_vars]
        simi = inv(sim[:, :num_vars])

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        assert nf <= maxfun, f'NF <= MAXFUN {srname}'
        assert evaluated.size == num_vars + 1, f'EVALUATED.size == Num_vars + 1 {srname}'
        # assert chist.size == maxchist, f'CHIST.size == MAXCHIST {srname}'
        # assert conhist.shape== (num_constraints, maxconhist), f'CONHIST.shape == [M, MAXCONHIST] {srname}'
        assert conmat.shape == (num_constraints, num_vars + 1), f'CONMAT.shape = [M, N+1] {srname}'
        assert not (np.isnan(conmat).any() or np.isneginf(conmat).any()), f'CONMAT does not contain NaN/-Inf {srname}'
        assert cval.size == num_vars + 1 and not (any(cval < 0) or any(np.isnan(cval)) or any(np.isposinf(cval))), f'CVAL.shape == Num_vars+1 and CVAL does not contain negative values or NaN/+Inf {srname}'
        # assert fhist.shape == maxfhist, f'FHIST.shape == MAXFHIST {srname}'
        # assert maxfhist * (maxfhist - maxhist) == 0, f'FHIST.shape == 0 or MAXHIST {srname}'
        assert fval.size == num_vars + 1 and not (any(np.isnan(fval)) or any(np.isposinf(fval))), f'FVAL.shape == Num_vars+1 and FVAL is not NaN/+Inf {srname}'
        # assert xhist.shape == (num_vars, maxxhist), f'XHIST.shape == [N, MAXXHIST] {srname}'
        assert sim.shape == (num_vars, num_vars + 1), f'SIM.shape == [N, N+1] {srname}'
        assert np.isfinite(sim).all(), f'SIM is finite {srname}'
        assert all(np.max(abs(sim[:, :num_vars]), axis=0) > 0), f'SIM(:, 1:N) has no zero column {srname}'
        assert simi.shape == (num_vars, num_vars), f'SIMI.shape == [N, N] {srname}'
        assert np.isfinite(simi).all(), f'SIMI is finite {srname}'
        assert np.allclose(sim[:, :num_vars] @ simi, np.eye(num_vars), rtol=0.1, atol=0.1) or not all(evaluated), f'SIMI = SIM(:, 1:N)^{-1} {srname}'

    return evaluated, conmat, cval, sim, simi, fval, nf, info

