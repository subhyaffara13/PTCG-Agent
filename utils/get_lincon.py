
def get_lincon(Aeq=None, Aineq=None, beq=None, bineq=None, xl=None, xu=None):
    """
    This subroutine wraps the linear and bound constraints into a single constraint:
        AMAT*X <= BVEC.

    N.B.:

    LINCOA normalizes the linear constraints so that each constraint has a gradient
    of norm 1. However, COBYLA does not do this.
    """

    # Sizes
    if Aeq is not None:
        num_vars = Aeq.shape[1]
    elif Aineq is not None:
        num_vars = Aineq.shape[1]
    elif xl is not None:
        num_vars = len(xl)
    elif xu is not None:
        num_vars = len(xu)
    else:
        return None, None

    # Preconditions
    if DEBUGGING:
        assert Aineq is None or Aineq.shape == (len(bineq), num_vars)
        assert Aeq is None or Aeq.shape == (len(beq), num_vars)
        assert (xl is None or xu is None) or len(xl) == len(xu) == num_vars

    #====================#
    # Calculation starts #
    #====================#

    # Define the indices of the nontrivial bound constraints.
    ixl = np.where(xl > -BOUNDMAX)[0] if xl is not None else None
    ixu = np.where(xu < BOUNDMAX)[0] if xu is not None else None

    # Wrap the linear constraints.
    # The bound constraint XL <= X <= XU is handled as two constraints:
    # -X <= -XL, X <= XU.
    # The equality constraint Aeq*X = Beq is handled as two constraints:
    # -Aeq*X <= -Beq, Aeq*X <= Beq.
    # N.B.:
    # 1. The treatment of the equality constraints is naive. One may choose to
    #    eliminate them instead.
    idmat = np.eye(num_vars)
    amat = np.vstack([
        -idmat[ixl, :] if ixl is not None else np.empty((0, num_vars)),
        idmat[ixu, :] if ixu is not None else np.empty((0, num_vars)),
        -Aeq if Aeq is not None else np.empty((0, num_vars)),
        Aeq if Aeq is not None else np.empty((0, num_vars)),
        Aineq if Aineq is not None else np.empty((0, num_vars))
    ])
    bvec = np.hstack([
        -xl[ixl] if ixl is not None else np.empty(0),
        xu[ixu] if ixu is not None else np.empty(0),
        -beq if beq is not None else np.empty(0),
        beq if beq is not None else np.empty(0),
        bineq if bineq is not None else np.empty(0)
    ])

    amat = amat if amat.shape[0] > 0 else None
    bvec = bvec if bvec.shape[0] > 0 else None

    #==================#
    # Calculation ends #
    #==================#

    # Postconditions
    if DEBUGGING:
        assert (amat is None and bvec is None) or amat.shape == (len(bvec), num_vars)

    return amat, bvec

