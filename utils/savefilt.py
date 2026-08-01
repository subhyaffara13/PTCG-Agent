
def savefilt(cstrv, ctol, cweight, f, x, nfilt, cfilt, ffilt, xfilt, constr=None, confilt=None):
    '''
    This subroutine saves X, F, and CSTRV in XFILT, FFILT, and CFILT (and CONSTR in CONFILT
    if they are present), unless a vector in XFILT[:, :NFILT] is better than X.
    If X is better than some vectors in XFILT[:, :NFILT] then these vectors will be
    removed. If X is not better than any of XFILT[:, :NFILT], but NFILT == MAXFILT,
    then we remove a column from XFILT according to the merit function
    PHI = FFILT + CWEIGHT * max(CFILT - CTOL, 0)
    N.B.:
    1. Only XFILT[:, :NFILT] and FFILT[:, :NFILT] etc contains valid information,
    while XFILT[:, NFILT+1:MAXFILT] and FFILT[:, NFILT+1:MAXFILT] etc are not
    initialized yet.
    2. We decide whether and X is better than another by the ISBETTER function
    '''

    # Sizes
    if present(constr):
        num_constraints = len(constr)
    else:
        num_constraints = 0
    num_vars = len(x)
    maxfilt = len(ffilt)

    # Preconditions
    if DEBUGGING:
        # Check the size of X.
        assert num_vars >= 1
        # Check CWEIGHT and CTOL
        assert cweight >= 0
        assert ctol >= 0
        # Check NFILT
        assert nfilt >= 0 and nfilt <= maxfilt
        # Check the sizes of XFILT, FFILT, CFILT.
        assert maxfilt >= 1
        assert np.size(xfilt, 0) == num_vars and np.size(xfilt, 1) == maxfilt
        assert np.size(cfilt) == maxfilt
        # Check the values of XFILT, FFILT, CFILT.
        assert not (np.isnan(xfilt[:, :nfilt])).any()
        assert not any(np.isnan(ffilt[:nfilt]) | np.isposinf(ffilt[:nfilt]))
        assert not any(cfilt[:nfilt] < 0 | np.isnan(cfilt[:nfilt]) | np.isposinf(cfilt[:nfilt]))
        # Check the values of X, F, CSTRV.
        # X does not contain NaN if X0 does not and the trust-region/geometry steps are proper.
        assert not any(np.isnan(x))
        # F cannot be NaN/+Inf due to the moderated extreme barrier.
        assert not (np.isnan(f) | np.isposinf(f))
        # CSTRV cannot be NaN/+Inf due to the moderated extreme barrier.
        assert not (cstrv < 0 | np.isnan(cstrv) | np.isposinf(cstrv))
        # Check CONSTR and CONFILT.
        assert present(constr) == present(confilt)
        if present(constr):
            # CONSTR cannot contain NaN/-Inf due to the moderated extreme barrier.
            assert not any(np.isnan(constr) | np.isneginf(constr))
            assert np.size(confilt, 0) == num_constraints and np.size(confilt, 1) == maxfilt
            assert not (np.isnan(confilt[:, :nfilt]) | np.isneginf(confilt[:, :nfilt])).any()

    #====================#
    # Calculation starts #
    #====================#

    # Return immediately if any column of XFILT is better than X.
    if any((isbetter(ffilt_i, cfilt_i, f, cstrv, ctol) for ffilt_i, cfilt_i in zip(ffilt[:nfilt], cfilt[:nfilt]))) or \
        any(np.logical_and(ffilt[:nfilt] <= f, cfilt[:nfilt] <= cstrv)):
        return nfilt, cfilt, ffilt, xfilt, confilt

    # Decide which columns of XFILT to keep.
    keep = np.logical_not([isbetter(f, cstrv, ffilt_i, cfilt_i, ctol) for ffilt_i, cfilt_i in zip(ffilt[:nfilt], cfilt[:nfilt])])

    # If NFILT == MAXFILT and X is not better than any column of XFILT, then we remove the worst column
    # of XFILT according to the merit function PHI = FFILT + CWEIGHT * MAX(CFILT - CTOL, ZERO).
    if sum(keep) == maxfilt:  # In this case, NFILT = SIZE(KEEP) = COUNT(KEEP) = MAXFILT > 0.
        cfilt_shifted = np.maximum(cfilt - ctol, 0)
        if cweight <= 0:
            phi = ffilt
        elif np.isposinf(cweight):
            phi = cfilt_shifted
            # We should not use CFILT here; if MAX(CFILT_SHIFTED) is attained at multiple indices, then
            # we will check FFILT to exhaust the remaining degree of freedom.
        else:
            phi = np.maximum(ffilt, -REALMAX)
            phi = np.nan_to_num(phi, nan=-REALMAX)  # Replace NaN with -REALMAX and +/- inf with large numbers
            phi += cweight * cfilt_shifted
        # We select X to maximize PHI. In case there are multiple maximizers, we take the one with the
        # largest CSTRV_SHIFTED; if there are more than one choices, we take the one with the largest F;
        # if there are several candidates, we take the one with the largest CSTRV; if the last comparison
        # still leads to more than one possibilities, then they are equally bad and we choose the first.
        # N.B.:
        # 1. This process is the opposite of selecting KOPT in SELECTX.
        # 2. In finite-precision arithmetic, PHI_1 == PHI_2 and CSTRV_SHIFTED_1 == CSTRV_SHIFTED_2 do
        # not ensure that F_1 == F_2!
        phimax = max(phi)
        cref = max(cfilt_shifted[phi >= phimax])
        fref = max(ffilt[cfilt_shifted >= cref])
        kworst = np.ma.array(cfilt, mask=(ffilt > fref)).argmax()
        if kworst < 0 or kworst >= len(keep):  #  For security. Should not happen.
            kworst = 0
        keep[kworst] = False

    # Keep the good xfilt values and remove all the ones that are strictly worse than the new x.
    nfilt = sum(keep)
    index_to_keep = np.where(keep)[0]
    xfilt[:, :nfilt] = xfilt[:, index_to_keep]
    ffilt[:nfilt] = ffilt[index_to_keep]
    cfilt[:nfilt] = cfilt[index_to_keep]
    if confilt is not None and constr is not None:
        confilt[:, :nfilt] = confilt[:, index_to_keep]

    # Once we have removed all the vectors that are strictly worse than x,
    # we add x to the filter.
    xfilt[:, nfilt] = x
    ffilt[nfilt] = f
    cfilt[nfilt] = cstrv
    if confilt is not None and constr is not None:
        confilt[:, nfilt] = constr
    nfilt += 1  # In Python we need to increment the index afterwards

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        # Check NFILT and the sizes of XFILT, FFILT, CFILT.
        assert nfilt >= 1 and nfilt <= maxfilt
        assert np.size(xfilt, 0) == num_vars and np.size(xfilt, 1) == maxfilt
        assert np.size(ffilt) == maxfilt
        assert np.size(cfilt) == maxfilt
        # Check the values of XFILT, FFILT, CFILT.
        assert not (np.isnan(xfilt[:, :nfilt])).any()
        assert not any(np.isnan(ffilt[:nfilt]) | np.isposinf(ffilt[:nfilt]))
        assert not any(cfilt[:nfilt] < 0 | np.isnan(cfilt[:nfilt]) | np.isposinf(cfilt[:nfilt]))
        # Check that no point in the filter is better than X, and X is better than no point.
        assert not any([isbetter(ffilt_i, cfilt_i, f, cstrv, ctol) for ffilt_i, cfilt_i in zip(ffilt[:nfilt], cfilt[:nfilt])])
        assert not any([isbetter(f, cstrv, ffilt_i, cfilt_i, ctol) for ffilt_i, cfilt_i in zip(ffilt[:nfilt], cfilt[:nfilt])])
        # Check CONFILT.
        if present(confilt):
            assert np.size(confilt, 0) == num_constraints and np.size(confilt, 1) == maxfilt
            assert not (np.isnan(confilt[:, :nfilt]) | np.isneginf(confilt[:, :nfilt])).any()


    return nfilt, cfilt, ffilt, xfilt, confilt

