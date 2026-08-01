
def try_lerchphi(func):
    """
    Try to find an expression for Hyper_Function ``func`` in terms of Lerch
    Transcendents.

    Return None if no such expression can be found.
    """
    # This is actually quite simple, and is described in Roach's paper,
    # section 18.
    # We don't need to implement the reduction to polylog here, this
    # is handled by expand_func.

    # First we need to figure out if the summation coefficient is a rational
    # function of the summation index, and construct that rational function.
    abuckets, bbuckets = sift(func.ap, _mod1), sift(func.bq, _mod1)

    paired = {}
    for key, value in abuckets.items():
        if key != 0 and key not in bbuckets:
            return None
        bvalue = bbuckets[key]
        paired[key] = (list(value), list(bvalue))
        bbuckets.pop(key, None)
    if bbuckets != {}:
        return None
    if S.Zero not in abuckets:
        return None
    aints, bints = paired[S.Zero]
    # Account for the additional n! in denominator
    paired[S.Zero] = (aints, bints + [1])

    t = Dummy('t')
    numer = S.One
    denom = S.One
    for key, (avalue, bvalue) in paired.items():
        if len(avalue) != len(bvalue):
            return None
        # Note that since order has been reduced fully, all the b are
        # bigger than all the a they differ from by an integer. In particular
        # if there are any negative b left, this function is not well-defined.
        for a, b in zip(avalue, bvalue):
            if (a - b).is_positive:
                k = a - b
                numer *= rf(b + t, k)
                denom *= rf(b, k)
            else:
                k = b - a
                numer *= rf(a, k)
                denom *= rf(a + t, k)

    # Now do a partial fraction decomposition.
    # We assemble two structures: a list monomials of pairs (a, b) representing
    # a*t**b (b a non-negative integer), and a dict terms, where
    # terms[a] = [(b, c)] means that there is a term b/(t-a)**c.
    part = apart(numer/denom, t)
    args = Add.make_args(part)
    monomials = []
    terms = {}
    for arg in args:
        numer, denom = arg.as_numer_denom()
        if not denom.has(t):
            p = Poly(numer, t)
            if not p.is_monomial:
                raise TypeError("p should be monomial")
            ((b, ), a) = p.LT()
            monomials += [(a/denom, b)]
            continue
        if numer.has(t):
            raise NotImplementedError('Need partial fraction decomposition'
                                      ' with linear denominators')
        indep, [dep] = denom.as_coeff_mul(t)
        n = 1
        if dep.is_Pow:
            n = dep.exp
            dep = dep.base
        if dep == t:
            a = 0
        elif dep.is_Add:
            a, tmp = dep.as_independent(t)
            b = 1
            if tmp != t:
                b, _ = tmp.as_independent(t)
            if dep != b*t + a:
                raise NotImplementedError('unrecognised form %s' % dep)
            a /= b
            indep *= b**n
        else:
            raise NotImplementedError('unrecognised form of partial fraction')
        terms.setdefault(a, []).append((numer/indep, n))

    # Now that we have this information, assemble our formula. All the
    # monomials yield rational functions and go into one basis element.
    # The terms[a] are related by differentiation. If the largest exponent is
    # n, we need lerchphi(z, k, a) for k = 1, 2, ..., n.
    # deriv maps a basis to its derivative, expressed as a C(z)-linear
    # combination of other basis elements.
    deriv = {}
    coeffs = {}
    z = Dummy('z')
    monomials.sort(key=lambda x: x[1])
    mon = {0: 1/(1 - z)}
    if monomials:
        for k in range(monomials[-1][1]):
            mon[k + 1] = z*mon[k].diff(z)
    for a, n in monomials:
        coeffs.setdefault(S.One, []).append(a*mon[n])
    for a, l in terms.items():
        for c, k in l:
            coeffs.setdefault(lerchphi(z, k, a), []).append(c)
        l.sort(key=lambda x: x[1])
        for k in range(2, l[-1][1] + 1):
            deriv[lerchphi(z, k, a)] = [(-a, lerchphi(z, k, a)),
                                        (1, lerchphi(z, k - 1, a))]
        deriv[lerchphi(z, 1, a)] = [(-a, lerchphi(z, 1, a)),
                                    (1/(1 - z), S.One)]
    trans = {}
    for n, b in enumerate([S.One] + list(deriv.keys())):
        trans[b] = n
    basis = [expand_func(b) for (b, _) in sorted(trans.items(),
                                                 key=lambda x:x[1])]
    B = Matrix(basis)
    C = Matrix([[0]*len(B)])
    for b, c in coeffs.items():
        C[trans[b]] = Add(*c)
    M = zeros(len(B))
    for b, l in deriv.items():
        for c, b2 in l:
            M[trans[b], trans[b2]] = c
    return Formula(func, z, None, [], B, C, M)

