
def _dirichlet_check_parameters(alpha):
    alpha = np.asarray(alpha)
    if np.min(alpha) <= 0:
        raise ValueError("All parameters must be greater than 0")
    elif alpha.ndim != 1:
        raise ValueError("Parameter vector 'a' must be one dimensional, "
                         f"but a.shape = {alpha.shape}.")
    return alpha

