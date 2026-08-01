
def parametric_log_deriv(fa, fd, wa, wd, DE):
    # TODO: Write the full algorithm using the structure theorems.
#    try:
    A = parametric_log_deriv_heu(fa, fd, wa, wd, DE)
#    except NotImplementedError:
        # Heuristic failed, we have to use the full method.
        # TODO: This could be implemented more efficiently.
        # It isn't too worrisome, because the heuristic handles most difficult
        # cases.
    return A

