
def try_shifted_sum(func, z):
    """ Try to recognise a hypergeometric sum that starts from k > 0. """
    abuckets, bbuckets = sift(func.ap, _mod1), sift(func.bq, _mod1)
    if len(abuckets[S.Zero]) != 1:
        return None
    r = abuckets[S.Zero][0]
    if r <= 0:
        return None
    if S.Zero not in bbuckets:
        return None
    l = list(bbuckets[S.Zero])
    l.sort()
    k = l[0]
    if k <= 0:
        return None

    nap = list(func.ap)
    nap.remove(r)
    nbq = list(func.bq)
    nbq.remove(k)
    k -= 1
    nap = [x - k for x in nap]
    nbq = [x - k for x in nbq]

    ops = []
    for n in range(r - 1):
        ops.append(ShiftA(n + 1))
    ops.reverse()

    fac = factorial(k)/z**k
    fac *= Mul(*[rf(b, k) for b in nbq])
    fac /= Mul(*[rf(a, k) for a in nap])

    ops += [MultOperator(fac)]

    p = 0
    for n in range(k):
        m = z**n/factorial(n)
        m *= Mul(*[rf(a, n) for a in nap])
        m /= Mul(*[rf(b, n) for b in nbq])
        p += m

    return Hyper_Function(nap, nbq), ops, -p

