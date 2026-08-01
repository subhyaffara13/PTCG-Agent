
def _bessel_zeros(N):
    """
    Find zeros of ordinary Bessel polynomial of order `N`, by root-finding of
    modified Bessel function of the second kind
    """
    if N == 0:
        return np.asarray([])

    # Generate starting points
    x0 = _campos_zeros(N)

    # Zeros are the same for exp(1/x)*K_{N+0.5}(1/x) and Nth-order ordinary
    # Bessel polynomial y_N(x)
    def f(x):
        return special.kve(N+0.5, 1/x)

    # First derivative of above
    def fp(x):
        return (special.kve(N-0.5, 1/x)/(2*x**2) -
                special.kve(N+0.5, 1/x)/(x**2) +
                special.kve(N+1.5, 1/x)/(2*x**2))

    # Starting points converge to true zeros
    x = _aberth(f, fp, x0)

    # Improve precision using Newton's method on each
    for i in range(len(x)):
        x[i] = optimize.newton(f, x[i], fp, tol=1e-15)

    # Average complex conjugates to make them exactly symmetrical
    x = np.mean((x, x[::-1].conj()), 0)

    # Zeros should sum to -1
    if abs(np.sum(x) + 1) > 1e-15:
        raise RuntimeError('Generated zeros are inaccurate')

    return x

