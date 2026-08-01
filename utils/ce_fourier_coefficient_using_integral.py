
def ce_fourier_coefficient_using_integral(k, n, q):
    """
    Compute the Fourier coefficient of the even Mathieu function.
    The integral definition of a Fourier coefficient is used.
    This function is used as an alternative implementation of
    mathieu_even_coef().
    """
    period = 180 if n % 2 == 0 else 360
    # For k = 0, the factor outside the integral is (1/period).
    # For k = 1, 2, 3, ..., the factor is (2/period).
    c = (1/period)*quad(lambda t: special.mathieu_cem(n, q, t)[0],
                        -period/2, period/2,
                        weight='cos', wvar=2*np.pi*k/period, epsrel=1e-14)[0]
    if k > 0:
        c *= 2
    return c

