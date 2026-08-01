
def _get_left_bracket(fun, rbrack, lbrack=None):
    # find left bracket for `root_scalar`. A guess for lbrack may be provided.
    lbrack = lbrack or rbrack - 1
    diff = rbrack - lbrack

    # if there is no sign change in `fun` between the brackets, expand
    # rbrack - lbrack until a sign change occurs
    def interval_contains_root(lbrack, rbrack):
        # return true if the signs disagree.
        return np.sign(fun(lbrack)) != np.sign(fun(rbrack))

    while not interval_contains_root(lbrack, rbrack):
        diff *= 2
        lbrack = rbrack - diff

        msg = ("The solver could not find a bracket containing a "
               "root to an MLE first order condition.")
        if np.isinf(lbrack):
            raise FitSolverError(msg)

    return lbrack

