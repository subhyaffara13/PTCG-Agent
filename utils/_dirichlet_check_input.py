
def _dirichlet_check_input(alpha, x):
    x = np.asarray(x)

    if x.shape[0] + 1 != alpha.shape[0] and x.shape[0] != alpha.shape[0]:
        raise ValueError("Vector 'x' must have either the same number "
                         "of entries as, or one entry fewer than, "
                         f"parameter vector 'a', but alpha.shape = {alpha.shape} "
                         f"and x.shape = {x.shape}.")

    if x.shape[0] != alpha.shape[0]:
        xk = np.array([1 - np.sum(x, 0)])
        if xk.ndim == 1:
            x = np.append(x, xk)
        elif xk.ndim == 2:
            x = np.vstack((x, xk))
        else:
            raise ValueError("The input must be one dimensional or a two "
                             "dimensional matrix containing the entries.")

    if np.min(x) < 0:
        raise ValueError("Each entry in 'x' must be greater than or equal "
                         "to zero.")

    if np.max(x) > 1:
        raise ValueError("Each entry in 'x' must be smaller or equal one.")

    # Check x_i > 0 or alpha_i > 1
    xeq0 = (x == 0)
    alphalt1 = (alpha < 1)
    if x.shape != alpha.shape:
        alphalt1 = np.repeat(alphalt1, x.shape[-1], axis=-1).reshape(x.shape)
    chk = np.logical_and(xeq0, alphalt1)

    if np.sum(chk):
        raise ValueError("Each entry in 'x' must be greater than zero if its "
                         "alpha is less than one.")

    if (np.abs(np.sum(x, 0) - 1.0) > 10e-10).any():
        raise ValueError("The input vector 'x' must lie within the normal "
                         f"simplex. but np.sum(x, 0) = {np.sum(x, 0)}.")

    return x

