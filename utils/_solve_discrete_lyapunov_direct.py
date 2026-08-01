
def _solve_discrete_lyapunov_direct(a, q):
    """
    Solves the discrete Lyapunov equation directly.

    This function is called by the `solve_discrete_lyapunov` function with
    `method=direct`. It is not supposed to be called directly.
    """

    lhs = np.kron(a, a.conj())
    lhs = np.eye(lhs.shape[0]) - lhs
    x = solve(lhs, q.flatten())

    return np.reshape(x, q.shape)

