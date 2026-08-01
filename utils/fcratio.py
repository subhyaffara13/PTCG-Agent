
def fcratio(conmat, fval):
    '''
    This function calculates the ratio between the "typical change" of F and that of CONSTR.
    See equations (12)-(13) in Section 3 of the COBYLA paper for the definition of the ratio.
    '''

    # Preconditions
    if DEBUGGING:
        assert np.size(fval) >= 1
        assert np.size(conmat, 1) == np.size(fval)

    #====================#
    # Calculation starts #
    #====================#

    cmin = np.min(-conmat, axis=1)
    cmax = np.max(-conmat, axis=1)
    fmin = min(fval)
    fmax = max(fval)
    if any(cmin < 0.5 * cmax) and fmin < fmax:
        denom = np.min(np.maximum(cmax, 0) - cmin, where=cmin < 0.5 * cmax, initial=np.inf)
        # Powell mentioned the following alternative in section 4 of his COBYLA paper. According to a test
        # on 20230610, it does not make much difference to the performance.
        # denom = np.max(max(*cmax, 0) - cmin, mask=(cmin < 0.5 * cmax))
        r = (fmax - fmin) / denom
    else:
        r = 0

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        assert r >= 0

    return r

