
def _aberth(f, fp, x0, tol=1e-15, maxiter=50):
    """
    Given a function `f`, its first derivative `fp`, and a set of initial
    guesses `x0`, simultaneously find the roots of the polynomial using the
    Aberth-Ehrlich method.

    ``len(x0)`` should equal the number of roots of `f`.

    (This is not a complete implementation of Bini's algorithm.)
    """

    N = len(x0)

    x = np.array(x0, complex)
    beta = np.empty_like(x0)

    for iteration in range(maxiter):
        alpha = -f(x) / fp(x)  # Newton's method

        # Model "repulsion" between zeros
        for k in range(N):
            beta[k] = np.sum(1/(x[k] - x[k+1:]))
            beta[k] += np.sum(1/(x[k] - x[:k]))

        x += alpha / (1 + alpha * beta)

        if not all(np.isfinite(x)):
            raise RuntimeError('Root-finding calculation failed')

        # Mekwi: The iterative process can be stopped when |hn| has become
        # less than the largest error one is willing to permit in the root.
        if all(abs(alpha) <= tol):
            break
    else:
        raise Exception('Zeros failed to converge')

    return x

