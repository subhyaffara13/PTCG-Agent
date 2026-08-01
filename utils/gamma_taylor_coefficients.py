
def gamma_taylor_coefficients(inprec):
    """
    Gives the Taylor coefficients of 1/gamma(1+x) as
    a list of fixed-point numbers. Enough coefficients are returned
    to ensure that the series converges to the given precision
    when x is in [0.5, 1.5].
    """
    # Reuse nearby cache values (small case)
    if inprec < 400:
        prec = inprec + (10-(inprec%10))
    elif inprec < 1000:
        prec = inprec + (30-(inprec%30))
    else:
        prec = inprec
    if prec in gamma_taylor_cache:
        return gamma_taylor_cache[prec], prec

    # Experimentally determined bounds
    if prec < 1000:
        N = int(prec**0.76 + 2)
    else:
        # Valid to at least 15000 bits
        N = int(prec**0.787 + 2)

    # Reuse higher precision values
    for cprec in gamma_taylor_cache:
        if cprec > prec:
            coeffs = [x>>(cprec-prec) for x in gamma_taylor_cache[cprec][-N:]]
            if inprec < 1000:
                gamma_taylor_cache[prec] = coeffs
            return coeffs, prec

    # Cache at a higher precision (large case)
    if prec > 1000:
        prec = int(prec * 1.2)

    wp = prec + 20
    A = [0] * N
    A[0] = MPZ_ZERO
    A[1] = MPZ_ONE << wp
    A[2] = euler_fixed(wp)
    # SLOW, reference implementation
    #zeta_values = [0,0]+[to_fixed(mpf_zeta_int(k,wp),wp) for k in xrange(2,N)]
    zeta_values = zeta_array(N, wp)
    for k in xrange(3, N):
        a = (-A[2]*A[k-1])>>wp
        for j in xrange(2,k):
            a += ((-1)**j * zeta_values[j] * A[k-j]) >> wp
        a //= (1-k)
        A[k] = a
    A = [a>>20 for a in A]
    A = A[::-1]
    A = A[:-1]
    gamma_taylor_cache[prec] = A
    #return A, prec
    return gamma_taylor_coefficients(inprec)

