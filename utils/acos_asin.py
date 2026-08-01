
def acos_asin(z, prec, rnd, n):
    """ complex acos for n = 0, asin for n = 1
    The algorithm is described in
    T.E. Hull, T.F. Fairgrieve and P.T.P. Tang
    'Implementing the Complex Arcsine and Arcosine Functions
    using Exception Handling',
    ACM Trans. on Math. Software Vol. 23 (1997), p299
    The complex acos and asin can be defined as
    acos(z) = acos(beta) - I*sign(a)* log(alpha + sqrt(alpha**2 -1))
    asin(z) = asin(beta) + I*sign(a)* log(alpha + sqrt(alpha**2 -1))
    where z = a + I*b
    alpha = (1/2)*(r + s); beta = (1/2)*(r - s) = a/alpha
    r = sqrt((a+1)**2 + y**2); s = sqrt((a-1)**2 + y**2)
    These expressions are rewritten in different ways in different
    regions, delimited by two crossovers alpha_crossover and beta_crossover,
    and by abs(a) <= 1, in order to improve the numerical accuracy.
    """
    a, b = z
    wp = prec + 10
    # special cases with real argument
    if b == fzero:
        am = mpf_sub(fone, mpf_abs(a), wp)
        # case abs(a) <= 1
        if not am[0]:
            if n == 0:
                return mpf_acos(a, prec, rnd), fzero
            else:
                return mpf_asin(a, prec, rnd), fzero
        # cases abs(a) > 1
        else:
            # case a < -1
            if a[0]:
                pi = mpf_pi(prec, rnd)
                c = mpf_acosh(mpf_neg(a), prec, rnd)
                if n == 0:
                    return pi, mpf_neg(c)
                else:
                    return mpf_neg(mpf_shift(pi, -1)), c
            # case a > 1
            else:
                c = mpf_acosh(a, prec, rnd)
                if n == 0:
                    return fzero, c
                else:
                    pi = mpf_pi(prec, rnd)
                    return mpf_shift(pi, -1), mpf_neg(c)
    asign = bsign = 0
    if a[0]:
        a = mpf_neg(a)
        asign = 1
    if b[0]:
        b = mpf_neg(b)
        bsign = 1
    am = mpf_sub(fone, a, wp)
    ap = mpf_add(fone, a, wp)
    r = mpf_hypot(ap, b, wp)
    s = mpf_hypot(am, b, wp)
    alpha = mpf_shift(mpf_add(r, s, wp), -1)
    beta = mpf_div(a, alpha, wp)
    b2 = mpf_mul(b,b, wp)
    # case beta <= beta_crossover
    if not mpf_sub(beta_crossover, beta, wp)[0]:
        if n == 0:
            re = mpf_acos(beta, wp)
        else:
            re = mpf_asin(beta, wp)
    else:
        # to compute the real part in this region use the identity
        # asin(beta) = atan(beta/sqrt(1-beta**2))
        # beta/sqrt(1-beta**2) = (alpha + a) * (alpha - a)
        # alpha + a is numerically accurate; alpha - a can have
        # cancellations leading to numerical inaccuracies, so rewrite
        # it in differente ways according to the region
        Ax = mpf_add(alpha, a, wp)
        # case a <= 1
        if not am[0]:
            # c = b*b/(r + (a+1)); d = (s + (1-a))
            # alpha - a = (1/2)*(c + d)
            # case n=0: re = atan(sqrt((1/2) * Ax * (c + d))/a)
            # case n=1: re = atan(a/sqrt((1/2) * Ax * (c + d)))
            c = mpf_div(b2, mpf_add(r, ap, wp), wp)
            d = mpf_add(s, am, wp)
            re = mpf_shift(mpf_mul(Ax, mpf_add(c, d, wp), wp), -1)
            if n == 0:
                re = mpf_atan(mpf_div(mpf_sqrt(re, wp), a, wp), wp)
            else:
                re = mpf_atan(mpf_div(a, mpf_sqrt(re, wp), wp), wp)
        else:
            # c = Ax/(r + (a+1)); d = Ax/(s - (1-a))
            # alpha - a = (1/2)*(c + d)
            # case n = 0: re = atan(b*sqrt(c + d)/2/a)
            # case n = 1: re = atan(a/(b*sqrt(c + d)/2)
            c = mpf_div(Ax, mpf_add(r, ap, wp), wp)
            d = mpf_div(Ax, mpf_sub(s, am, wp), wp)
            re = mpf_shift(mpf_add(c, d, wp), -1)
            re = mpf_mul(b, mpf_sqrt(re, wp), wp)
            if n == 0:
                re = mpf_atan(mpf_div(re, a, wp), wp)
            else:
                re = mpf_atan(mpf_div(a, re, wp), wp)
    # to compute alpha + sqrt(alpha**2 - 1), if alpha <= alpha_crossover
    # replace it with 1 + Am1 + sqrt(Am1*(alpha+1)))
    # where Am1 = alpha -1
    # if alpha <= alpha_crossover:
    if not mpf_sub(alpha_crossover, alpha, wp)[0]:
        c1 = mpf_div(b2, mpf_add(r, ap, wp), wp)
        # case a < 1
        if mpf_neg(am)[0]:
            # Am1 = (1/2) * (b*b/(r + (a+1)) + b*b/(s + (1-a))
            c2 = mpf_add(s, am, wp)
            c2 = mpf_div(b2, c2, wp)
            Am1 = mpf_shift(mpf_add(c1, c2, wp), -1)
        else:
            # Am1 = (1/2) * (b*b/(r + (a+1)) + (s - (1-a)))
            c2 = mpf_sub(s, am, wp)
            Am1 = mpf_shift(mpf_add(c1, c2, wp), -1)
        # im = log(1 + Am1 + sqrt(Am1*(alpha+1)))
        im = mpf_mul(Am1, mpf_add(alpha, fone, wp), wp)
        im = mpf_log(mpf_add(fone, mpf_add(Am1, mpf_sqrt(im, wp), wp), wp), wp)
    else:
        # im = log(alpha + sqrt(alpha*alpha - 1))
        im = mpf_sqrt(mpf_sub(mpf_mul(alpha, alpha, wp), fone, wp), wp)
        im = mpf_log(mpf_add(alpha, im, wp), wp)
    if asign:
        if n == 0:
            re = mpf_sub(mpf_pi(wp), re, wp)
        else:
            re = mpf_neg(re)
    if not bsign and n == 0:
        im = mpf_neg(im)
    if bsign and n == 1:
        im = mpf_neg(im)
    re = normalize(re[0], re[1], re[2], re[3], prec, rnd)
    im = normalize(im[0], im[1], im[2], im[3], prec, rnd)
    return re, im

