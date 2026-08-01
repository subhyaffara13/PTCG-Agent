
def isbetter(f1: float, c1: float, f2: float, c2: float, ctol: float) -> bool:
    '''
    This function compares whether FC1 = (F1, C1) is (strictly) better than FC2 = (F2, C2), which
    basically means that (F1 < F2 and C1 <= C2) or (F1 <= F2 and C1 < C2).
    It takes care of the cases where some of these values are NaN or Inf, even though some cases
    should never happen due to the moderated extreme barrier.
    At return, BETTER = TRUE if and only if (F1, C1) is better than (F2, C2).
    Here, C means constraint violation, which is a nonnegative number.
    '''

    # Preconditions
    if DEBUGGING:
        assert not any(np.isnan([f1, c1]) | np.isposinf([f2, c2]))
        assert not any(np.isnan([f2, c2]) | np.isposinf([f2, c2]))
        assert c1 >= 0 and c2 >= 0
        assert ctol >= 0

    #====================#
    # Calculation starts #
    #====================#

    is_better = False
    # Even though NaN/+Inf should not occur in FC1 or FC2 due to the moderated extreme barrier, for
    # security and robustness, the code below does not make this assumption.
    is_better = is_better or (any(np.isnan([f1, c1]) | np.isposinf([f1, c1])) and not any(np.isnan([f2, c2]) | np.isposinf([f2, c2])))

    is_better = is_better or (f1 < f2 and c1 <= c2)
    is_better = is_better or (f1 <= f2 and c1 < c2)

    # If C1 <= CTOL and C2 is significantly larger/worse than CTOL, i.e., C2 > MAX(CTOL,CREF),
    # then FC1 is better than FC2 as long as F1 < REALMAX. Normally CREF >= CTOL so MAX(CTOL, CREF)
    # is indeed CREF. However, this may not be true if CTOL > 1E-1*CONSTRMAX.
    cref = 10 * max(EPS, min(ctol, 1.0E-2 * CONSTRMAX))  # The MIN avoids overflow.
    is_better = is_better or (f1 < REALMAX and c1 <= ctol and (c2 > max(ctol, cref) or np.isnan(c2)))

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        assert not (is_better and f1 >= f2 and c1 >= c2)
        assert is_better or not (f1 <= f2 and c1 < c2)
        assert is_better or not (f1 < f2 and c1 <= c2)

    return is_better

