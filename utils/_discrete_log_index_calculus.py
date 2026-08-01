
def _discrete_log_index_calculus(n, a, b, order, rseed=None):
    """
    Index Calculus algorithm for computing the discrete logarithm of ``a`` to
    the base ``b`` modulo ``n``.

    The group order must be given and prime. It is not suitable for small orders
    and the algorithm might fail to find a solution in such situations.

    Examples
    ========

    >>> from sympy.ntheory.residue_ntheory import _discrete_log_index_calculus
    >>> _discrete_log_index_calculus(24570203447, 23859756228, 2, 12285101723)
    4519867240

    See Also
    ========

    discrete_log

    References
    ==========

    .. [1] "Handbook of applied cryptography", Menezes, A. J., Van, O. P. C., &
        Vanstone, S. A. (1997).
    """
    randint = _randint(rseed)
    from math import sqrt, exp, log
    a %= n
    b %= n
    # assert isprime(order), "The order of the base must be prime."
    # First choose a heuristic the bound B for the factorbase.
    # We have added an extra term to the asymptotic value which
    # is closer to the theoretical optimum for n up to 2^70.
    B = int(exp(0.5 * sqrt( log(n) * log(log(n)) )*( 1 + 1/log(log(n)) )))
    max = 5 * B * B  # expected number of tries to find a relation
    factorbase = list(primerange(B)) # compute the factorbase
    lf = len(factorbase) # length of the factorbase
    ordermo = order-1
    abx = a
    for x in range(order):
        if abx == 1:
            return (order - x) % order
        relationa = _discrete_log_is_smooth(abx, factorbase)
        if relationa:
            relationa = [r % order for r in relationa] + [x]
            break
        abx = abx * b % n # abx = a*pow(b, x, n) % n

    else:
        raise ValueError("Index Calculus failed")

    relations = [None] * lf
    k = 1  # number of relations found
    kk = 0
    while k < 3 * lf and kk < max:  # find relations for all primes in our factor base
        x = randint(1,ordermo)
        relation = _discrete_log_is_smooth(pow(b,x,n), factorbase)
        if relation is None:
            kk += 1
            continue
        k += 1
        kk = 0
        relation += [ x ]
        index = lf  # determine the index of the first nonzero entry
        for i in range(lf):
            ri = relation[i] % order
            if ri> 0 and relations[i] is not None:  # make this entry zero if we can
                for j in range(lf+1):
                    relation[j] = (relation[j] - ri*relations[i][j]) % order
            else:
                relation[i] = ri
            if relation[i] > 0 and index == lf:  # is this the index of the first nonzero entry?
                index = i
        if index == lf or relations[index] is not None:  # the relation contains no new information
            continue
        # the relation contains new information
        rinv = pow(relation[index],-1,order)  # normalize the first nonzero entry
        for j in range(index,lf+1):
            relation[j] = rinv * relation[j] % order
        relations[index] = relation
        for i in range(lf):  # subtract the new relation from the one for a
            if relationa[i] > 0 and relations[i] is not None:
                rbi = relationa[i]
                for j in range(lf+1):
                    relationa[j] = (relationa[j] - rbi*relations[i][j]) % order
            if relationa[i] > 0:  # the index of the first nonzero entry
                break  # we do not need to reduce further at this point
        else:  # all unknowns are gone
            #print(f"Success after {k} relations out of {lf}")
            x = (order -relationa[lf]) % order
            if pow(b,x,n) == a:
                return x
            raise ValueError("Index Calculus failed")
    raise ValueError("Index Calculus failed")

