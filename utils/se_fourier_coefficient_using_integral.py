
def se_fourier_coefficient_using_integral(k, n, q):
    """
    Compute the Fourier coefficient of the odd Mathieu function.
    The integral definition of a Fourier coefficient is used.
    This function is used as an alternative implementation of
    mathieu_odd_coef().
    """
    # For k == 0, the result is 0. (The test code won't call this
    # function with k == 0, but we'll check anyway.)
    if k == 0:
        return 0.0
    period = 180 if n % 2 == 0 else 360
    c = (2/period)*quad(lambda t: special.mathieu_sem(n, q, t)[0],
                        -period/2, period/2,
                        weight='sin', wvar=2*np.pi*k/period, epsrel=1e-14)[0]
    return c

