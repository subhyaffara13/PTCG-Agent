
def getcpen(amat, bvec, conmat, cpen, cval, delta, fval, rho, sim, simi):
    '''
    This function gets the penalty parameter CPEN so that PREREM = PREREF + CPEN * PREREC > 0.
    See the discussions around equation (9) of the COBYLA paper.
    '''

    # Even after nearly all of the pycutest problems were showing nearly bit for bit
    # identical results between Python and the Fortran bindings, HS102 was still off by
    # more than machine epsilon. It turned out to be due to the fact that getcpen was
    # modifying fval, among other. It just goes to show that even when you're nearly
    # perfect, you can still have non trivial bugs.
    conmat = conmat.copy()
    cval = cval.copy()
    fval = fval.copy()
    sim = sim.copy()
    simi = simi.copy()

    # Intermediate variables
    A = np.zeros((np.size(sim, 0), np.size(conmat, 0)))
    itol = 1

    # Sizes
    m_lcon = np.size(bvec) if bvec is not None else 0
    num_constraints = np.size(conmat, 0)
    num_vars = np.size(sim, 0)

    # Preconditions
    if DEBUGGING:
        assert num_constraints >= 0
        assert num_vars >= 1
        assert cpen > 0
        assert np.size(conmat, 0) == num_constraints and np.size(conmat, 1) == num_vars + 1
        assert not (np.isnan(conmat) | np.isneginf(conmat)).any()
        assert np.size(cval) == num_vars + 1 and \
            not any(cval < 0 | np.isnan(cval) | np.isposinf(cval))
        assert np.size(fval) == num_vars + 1 and not any(np.isnan(fval) | np.isposinf(fval))
        assert np.size(sim, 0) == num_vars and np.size(sim, 1) == num_vars + 1
        assert np.isfinite(sim).all()
        assert all(np.max(abs(sim[:, :num_vars]), axis=0) > 0)
        assert np.size(simi, 0) == num_vars and np.size(simi, 1) == num_vars
        assert np.isfinite(simi).all()
        assert isinv(sim[:, :num_vars], simi, itol)
        assert delta >= rho and rho > 0

    #====================#
    # Calculation starts #
    #====================#

    # Initialize INFO which is needed in the postconditions
    info = INFO_DEFAULT

    # Increase CPEN if necessary to ensure PREREM > 0. Branch back for the next loop
    # if this change alters the optimal vertex of the current simplex.
    # Note the following:
    # 1. In each loop, CPEN is changed only if PREREC > 0 > PREREF, in which case
    #    PREREM is guaranteed positive after the update. Note that PREREC >= 0 and
    #    max(PREREC, PREREF) > 0 in theory. If this holds numerically as well then CPEN
    #    is not changed only if PREREC = 0 or PREREF >= 0, in which case PREREM is
    #    currently positive, explaining why CPEN needs no update.
    # 2. Even without an upper bound for the loop counter, the loop can occur at most
    #    NUM_VARS+1 times. This is because the update of CPEN does not decrease CPEN,
    #    and hence it can make vertex J (J <= NUM_VARS) become the new optimal vertex
    #    only if CVAL[J] is less than CVAL[NUM_VARS], which can happen at most NUM_VARS
    #    times. See the paragraph below (9) in the COBYLA paper. After the "correct"
    #    optimal vertex is found, one more loop is needed to calculate CPEN, and hence
    #    the loop can occur at most NUM_VARS+1 times.
    for iter in range(num_vars + 1):
        # Switch the best vertex of the current simplex to SIM[:, NUM_VARS]
        conmat, cval, fval, sim, simi, info = updatepole(cpen, conmat, cval, fval, sim,
                                                         simi)
        # Check whether to exit due to damaging rounding in UPDATEPOLE
        if info == DAMAGING_ROUNDING:
            break

        # Calculate the linear approximations to the objective and constraint functions.
        g = matprod(fval[:num_vars] - fval[num_vars], simi)
        A[:, :m_lcon] = amat.T if amat is not None else amat
        A[:, m_lcon:] = matprod((conmat[m_lcon:, :num_vars] -
                          np.tile(conmat[m_lcon:, num_vars], (num_vars, 1)).T), simi).T

        # Calculate the trust-region trial step D. Note that D does NOT depend on CPEN.
        d = trstlp(A, -conmat[:, num_vars], delta, g)

        # Predict the change to F (PREREF) and to the constraint violation (PREREC) due
        # to D.
        preref = -inprod(d, g)  # Can be negative
        prerec = cval[num_vars] - np.max(np.append(0, conmat[:, num_vars] + matprod(d, A)))

        # PREREC <= 0 or PREREF >=0 or either is NaN
        if not (prerec > 0 and preref < 0):
            break

        # Powell's code defines BARMU = -PREREF / PREREC, and CPEN is increased to
        # 2*BARMU if and only if it is currently less than 1.5*BARMU, a very
        # "Powellful" scheme. In our implementation, however, we set CPEN directly to
        # the maximum between its current value and 2*BARMU while handling possible
        # overflow. The simplifies the scheme without worsening the performance of
        # COBYLA.
        cpen = max(cpen, min(-2 * preref / prerec, REALMAX))

        if findpole(cpen, cval, fval) == num_vars:
            break

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        assert cpen >= cpen and cpen > 0
        assert preref + cpen * prerec > 0 or info == DAMAGING_ROUNDING or \
            not (prerec >= 0 and np.maximum(prerec, preref) > 0) or not np.isfinite(preref)

    return cpen

