
def fhtcoeff(n, dln, mu, offset=0.0, bias=0.0, inverse=False):
    """Compute the coefficient array for a fast Hankel transform."""
    lnkr, q = offset, bias

    # Hankel transform coefficients
    # u_m = (kr)^{-i 2m pi/(n dlnr)} U_mu(q + i 2m pi/(n dlnr))
    # with U_mu(x) = 2^x Gamma((mu+1+x)/2)/Gamma((mu+1-x)/2)
    xp = (mu+1+q)/2
    xm = (mu+1-q)/2
    y = np.linspace(0, np.pi*(n//2)/(n*dln), n//2+1)
    u = np.empty(n//2+1, dtype=complex)
    v = np.empty(n//2+1, dtype=complex)
    u.imag[:] = y
    u.real[:] = xm
    loggamma(u, out=v)
    u.real[:] = xp
    loggamma(u, out=u)
    y *= 2*(LN_2 - lnkr)
    u.real -= v.real
    u.real += LN_2*q
    u.imag += v.imag
    u.imag += y
    np.exp(u, out=u)

    # fix last coefficient to be real
    if n % 2 == 0:
        u.imag[-1] = 0

    # deal with special cases
    if not np.isfinite(u[0]):
        # write u_0 = 2^q Gamma(xp)/Gamma(xm) = 2^q poch(xm, xp-xm)
        # poch() handles special cases for negative integers correctly
        u[0] = 2**q * poch(xm, xp-xm)
        # the coefficient may be inf or 0, meaning the transform or the
        # inverse transform, respectively, is singular

    # check for singular transform or singular inverse transform
    if np.isinf(u[0]) and not inverse:
        warn('singular transform; consider changing the bias', stacklevel=3)
        # fix coefficient to obtain (potentially correct) transform anyway
        u = np.copy(u)
        u[0] = 0
    elif u[0] == 0 and inverse:
        warn('singular inverse transform; consider changing the bias', stacklevel=3)
        # fix coefficient to obtain (potentially correct) inverse anyway
        u = np.copy(u)
        u[0] = np.inf

    return u

