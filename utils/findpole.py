
def findpole(cpen, cval, fval):
    '''
    This subroutine identifies the best vertex of the current simplex with respect to the merit
    function PHI = F + CPEN * CSTRV.
    '''

    # Size
    num_vars = np.size(fval) - 1

    # Preconditions
    if DEBUGGING:
        assert cpen > 0
        assert np.size(cval) == num_vars + 1 and not any(cval < 0 | np.isnan(cval) | np.isposinf(cval))
        assert np.size(fval) == num_vars + 1 and not any(np.isnan(fval) | np.isposinf(fval))

    #====================#
    # Calculation starts #
    #====================#

    # Identify the optimal vertex of the current simplex
    jopt = np.size(fval) - 1
    phi = fval + cpen * cval
    phimin = min(phi)
    # Essentially jopt = np.argmin(phi). However, we keep jopt = num_vars unless there
    # is a strictly better choice. When there are multiple choices, we choose the jopt
    # with the smallest value of cval.
    if phimin < phi[jopt] or any((cval < cval[jopt]) & (phi <= phi[jopt])):
        # While we could use argmin(phi), there may be two places where phi achieves
        # phimin, and in that case we should choose the one with the smallest cval.
        jopt = np.ma.array(cval, mask=(phi > phimin)).argmin()

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        assert jopt >= 0 and jopt < num_vars + 1
        assert jopt == num_vars or phi[jopt] < phi[num_vars] or (phi[jopt] <= phi[num_vars] and cval[jopt] < cval[num_vars])
    return jopt

