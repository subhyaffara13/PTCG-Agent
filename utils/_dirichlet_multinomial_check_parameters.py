
def _dirichlet_multinomial_check_parameters(alpha, n, x=None):

    alpha = np.asarray(alpha)
    n = np.asarray(n)

    if x is not None:
        # Ensure that `x` and `alpha` are arrays. If the shapes are
        # incompatible, NumPy will raise an appropriate error.
        try:
            x, alpha = np.broadcast_arrays(x, alpha)
        except ValueError as e:
            msg = "`x` and `alpha` must be broadcastable."
            raise ValueError(msg) from e

        x_int = np.floor(x)
        if np.any(x < 0) or np.any(x != x_int):
            raise ValueError("`x` must contain only non-negative integers.")
        x = x_int

    if np.any(alpha <= 0):
        raise ValueError("`alpha` must contain only positive values.")

    n_int = np.floor(n)
    if np.any(n < 0) or np.any(n != n_int):
        raise ValueError("`n` must be a non-negative integer.")
    n = n_int

    sum_alpha = np.sum(alpha, axis=-1)
    sum_alpha, n = np.broadcast_arrays(sum_alpha, n)

    return (alpha, sum_alpha, n) if x is None else (alpha, sum_alpha, n, x)

