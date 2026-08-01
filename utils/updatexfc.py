
def updatexfc(jdrop, constr, cpen, cstrv, d, f, conmat, cval, fval, sim, simi):
    '''
    This function revises the simplex by updating the elements of SIM, SIMI, FVAL, CONMAT, and CVAL
    '''

    # Local variables
    itol = 1

    # Sizes
    num_constraints = np.size(constr)
    num_vars = np.size(sim, 0)

    # Preconditions
    if DEBUGGING:
        assert num_constraints >= 0
        assert num_vars >= 1
        assert jdrop >= 0 and jdrop <= num_vars + 1
        assert not any(np.isnan(constr) | np.isneginf(constr))
        assert not (np.isnan(cstrv) | np.isposinf(cstrv))
        assert np.size(d) == num_vars and all(np.isfinite(d))
        assert not (np.isnan(f) | np.isposinf(f))
        assert np.size(conmat, 0) == num_constraints and np.size(conmat, 1) == num_vars + 1
        assert not (np.isnan(conmat) | np.isneginf(conmat)).any()
        assert np.size(cval) == num_vars + 1 and not any(cval < 0 | np.isnan(cval) | np.isposinf(cval))
        assert np.size(fval) == num_vars + 1 and not any(np.isnan(fval) | np.isposinf(fval))
        assert np.size(sim, 0) == num_vars and np.size(sim, 1) == num_vars + 1
        assert np.isfinite(sim).all()
        assert all(primasum(abs(sim[:, :num_vars]), axis=0) > 0)
        assert np.size(simi, 0) == num_vars and np.size(simi, 1) == num_vars
        assert np.isfinite(simi).all()
        assert isinv(sim[:, :num_vars], simi, itol)

    #====================#
    # Calculation starts #
    #====================#


    # Do nothing when JDROP is None. This can only happen after a trust-region step.
    if jdrop is None:  # JDROP is None is impossible if the input is correct.
        return conmat, cval, fval, sim, simi, INFO_DEFAULT

    sim_old = sim
    simi_old = simi
    if jdrop < num_vars:
        sim[:, jdrop] = d
        simi_jdrop = simi[jdrop, :] / inprod(simi[jdrop, :], d)
        simi -= outprod(matprod(simi, d), simi_jdrop)
        simi[jdrop, :] = simi_jdrop
    else:  # jdrop == num_vars
        sim[:, num_vars] += d
        sim[:, :num_vars] -= np.tile(d, (num_vars, 1)).T
        simid = matprod(simi, d)
        sum_simi = primasum(simi, axis=0)
        simi += outprod(simid, sum_simi / (1 - sum(simid)))

    # Check whether SIMI is a poor approximation to the inverse of SIM[:, :NUM_VARS]
    # Calculate SIMI from scratch if the current one is damaged by rounding errors.
    itol = 1
    erri = np.max(abs(matprod(simi, sim[:, :num_vars]) - np.eye(num_vars)))  # np.max returns NaN if any input is NaN
    if erri > 0.1 * itol or np.isnan(erri):
        simi_test = inv(sim[:, :num_vars])
        erri_test = np.max(abs(matprod(simi_test, sim[:, :num_vars]) - np.eye(num_vars)))
        if erri_test < erri or (np.isnan(erri) and not np.isnan(erri_test)):
            simi = simi_test
            erri = erri_test

    # If SIMI is satisfactory, then update FVAL, CONMAT, CVAL, and the pole position. Otherwise restore
    # SIM and SIMI, and return with INFO = DAMAGING_ROUNDING.
    if erri <= itol:
        fval[jdrop] = f
        conmat[:, jdrop] = constr
        cval[jdrop] = cstrv
        # Switch the best vertex to the pole position SIM[:, NUM_VARS] if it is not there already
        conmat, cval, fval, sim, simi, info = updatepole(cpen, conmat, cval, fval, sim, simi)
    else:
        info = DAMAGING_ROUNDING
        sim = sim_old
        simi = simi_old

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        assert np.size(conmat, 0) == num_constraints and np.size(conmat, 1) == num_vars + 1
        assert not (np.isnan(conmat) | np.isneginf(conmat)).any()
        assert np.size(cval) == num_vars + 1 and not any(cval < 0 | np.isnan(cval) | np.isposinf(cval))
        assert np.size(fval) == num_vars + 1 and not any(np.isnan(fval) | np.isposinf(fval))
        assert np.size(sim, 0) == num_vars and np.size(sim, 1) == num_vars + 1
        assert np.isfinite(sim).all()
        assert all(primasum(abs(sim[:, :num_vars]), axis=0) > 0)
        assert np.size(simi, 0) == num_vars and np.size(simi, 1) == num_vars
        assert np.isfinite(simi).all()
        assert isinv(sim[:, :num_vars], simi, itol) or info == DAMAGING_ROUNDING

    return sim, simi, fval, conmat, cval, info

