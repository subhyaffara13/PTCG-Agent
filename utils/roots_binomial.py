
def roots_binomial(f):
    """Returns a list of roots of a binomial polynomial. If the domain is ZZ
    then the roots will be sorted with negatives coming before positives.
    The ordering will be the same for any numerical coefficients as long as
    the assumptions tested are correct, otherwise the ordering will not be
    sorted (but will be canonical).
    """
    n = f.degree()

    a, b = f.nth(n), f.nth(0)
    base = -cancel(b/a)
    alpha = root(base, n)

    if alpha.is_number:
        alpha = alpha.expand(complex=True)

    # define some parameters that will allow us to order the roots.
    # If the domain is ZZ this is guaranteed to return roots sorted
    # with reals before non-real roots and non-real sorted according
    # to real part and imaginary part, e.g. -1, 1, -1 + I, 2 - I
    neg = base.is_negative
    even = n % 2 == 0
    if neg:
        if even == True and (base + 1).is_positive:
            big = True
        else:
            big = False

    # get the indices in the right order so the computed
    # roots will be sorted when the domain is ZZ
    ks = []
    imax = n//2
    if even:
        ks.append(imax)
        imax -= 1
    if not neg:
        ks.append(0)
    for i in range(imax, 0, -1):
        if neg:
            ks.extend([i, -i])
        else:
            ks.extend([-i, i])
    if neg:
        ks.append(0)
        if big:
            for i in range(0, len(ks), 2):
                pair = ks[i: i + 2]
                pair = list(reversed(pair))

    # compute the roots
    roots, d = [], 2*I*pi/n
    for k in ks:
        zeta = exp(k*d).expand(complex=True)
        roots.append((alpha*zeta).expand(power_base=False))

    return roots

