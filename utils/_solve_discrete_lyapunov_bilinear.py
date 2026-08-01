
def _solve_discrete_lyapunov_bilinear(a, q):
    """
    Solves the discrete Lyapunov equation using a bilinear transformation.

    This function is called by the `solve_discrete_lyapunov` function with
    `method=bilinear`. It is not supposed to be called directly.
    """
    eye = np.eye(a.shape[0])
    aH = a.conj().transpose()
    aHI_inv = inv(aH + eye)
    b = np.dot(aH - eye, aHI_inv)
    c = 2*np.dot(np.dot(inv(a + eye), q), aHI_inv)
    return solve_lyapunov(b.conj().transpose(), -c)

