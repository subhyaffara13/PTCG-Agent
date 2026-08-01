
def initfilt(conmat, ctol, cweight, cval, fval, sim, evaluated, cfilt, confilt, ffilt, xfilt):
    '''
    This function initializes the filter (XFILT, etc) that will be used when selecting
    x at the end of the solver.
    N.B.:
    1. Why not initialize the filters using XHIST, etc? Because the history is empty if
    the user chooses not to output it.
    2. We decouple INITXFC and INITFILT so that it is easier to parallelize the former
    if needed.
    '''

    # Sizes
    num_constraints = conmat.shape[0]
    num_vars = sim.shape[0]
    maxfilt = len(ffilt)

    # Preconditions
    if DEBUGGING:
        assert num_constraints >= 0
        assert num_vars >= 1
        assert maxfilt >= 1
        assert np.size(confilt, 0) == num_constraints and np.size(confilt, 1) == maxfilt
        assert np.size(cfilt) == maxfilt
        assert np.size(xfilt, 0) == num_vars and np.size(xfilt, 1) == maxfilt
        assert np.size(ffilt) == maxfilt
        assert np.size(conmat, 0) == num_constraints and np.size(conmat, 1) == num_vars + 1
        assert not (np.isnan(conmat) | np.isneginf(conmat)).any()
        assert np.size(cval) == num_vars + 1 and not any(cval < 0 | np.isnan(cval) | np.isposinf(cval))
        assert np.size(fval) == num_vars + 1 and not any(np.isnan(fval) | np.isposinf(fval))
        assert np.size(sim, 0) == num_vars and np.size(sim, 1) == num_vars + 1
        assert np.isfinite(sim).all()
        assert all(np.max(abs(sim[:, :num_vars]), axis=0) > 0)
        assert np.size(evaluated) == num_vars + 1

    #====================#
    # Calculation starts #
    #====================#


    nfilt = 0
    for i in range(num_vars+1):
        if evaluated[i]:
            if i < num_vars:
                x = sim[:, i] + sim[:, num_vars]
            else:
                x = sim[:, i]  # i == num_vars, i.e. the last column
            nfilt, cfilt, ffilt, xfilt, confilt = savefilt(cval[i], ctol, cweight, fval[i], x, nfilt, cfilt, ffilt, xfilt, conmat[:, i], confilt)

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        assert nfilt <= maxfilt
        assert np.size(confilt, 0) == num_constraints and np.size(confilt, 1) == maxfilt
        assert not (np.isnan(confilt[:, :nfilt]) | np.isneginf(confilt[:, :nfilt])).any()
        assert np.size(cfilt) == maxfilt
        assert not any(cfilt[:nfilt] < 0 | np.isnan(cfilt[:nfilt]) | np.isposinf(cfilt[:nfilt]))
        assert np.size(xfilt, 0) == num_vars and np.size(xfilt, 1) == maxfilt
        assert not (np.isnan(xfilt[:, :nfilt])).any()
        # The last calculated X can be Inf (finite + finite can be Inf numerically).
        assert np.size(ffilt) == maxfilt
        assert not any(np.isnan(ffilt[:nfilt]) | np.isposinf(ffilt[:nfilt]))

    return nfilt

