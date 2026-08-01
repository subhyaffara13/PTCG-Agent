
def _partition(n: int) -> int:
    """ Calculate the partition function P(n)

    Parameters
    ==========

    n : int

    """
    if n < 0:
        return 0
    if (n <= 200_000 and n - _partition_rec.cache_length() < 70 or
            _partition_rec.cache_length() == 2 and n < 14_400):
        # There will be 2*10**5 elements created here
        # and n elements created by partition, so in case we
        # are going to be working with small n, we just
        # use partition to calculate (and cache) the values
        # since lookup is used there while summation, using
        # _factor and _totient, will be used below. But we
        # only do so if n is relatively close to the length
        # of the cache since doing 1 calculation here is about
        # the same as adding 70 elements to the cache. In addition,
        # the startup here costs about the same as calculating the first
        # 14,400 values via partition, so we delay startup here unless n
        # is smaller than that.
        return _partition_rec(n)
    if '_factor' not in globals():
        _pre()
    # Estimate number of bits in p(n). This formula could be tidied
    pbits = int((
        math.pi*(2*n/3.)**0.5 -
        math.log(4*n))/math.log(10) + 1) * \
        math.log2(10)
    prec = p = int(pbits*1.1 + 100)

    # find the number of terms needed so rounded sum will be accurate
    # using Rademacher's bound M(n, N) for the remainder after a partial
    # sum of N terms (https://arxiv.org/pdf/1205.5991.pdf, (1.8))
    c1 = 44*math.pi**2/(225*math.sqrt(3))
    c2 = math.pi*math.sqrt(2)/75
    c3 = math.pi*math.sqrt(2/3)
    def _M(n, N):
        sqrt = math.sqrt
        return c1/sqrt(N) + c2*sqrt(N/(n - 1))*math.sinh(c3*sqrt(n)/N)
    big = max(9, math.ceil(n**0.5))  # should be too large (for n > 65, ceil should work)
    assert _M(n, big) < 0.5  # else double big until too large
    while big > 40 and _M(n, big) < 0.5:
        big //= 2
    small = big
    big = small*2
    while big - small > 1:
        N = (big + small)//2
        if (er := _M(n, N)) < 0.5:
            big = N
        elif er >= 0.5:
            small = N
    M = big  # done with function M; now have value

    # sanity check for expected size of answer
    if M > 10**5:  # i.e. M > maxn
        raise ValueError("Input too big")  # i.e. n > 149832547102

    # calculate it
    s = fzero
    sq23pi = mpf_mul(mpf_sqrt(from_rational(2, 3, p), p), mpf_pi(p), p)
    sqrt8 = mpf_sqrt(from_int(8), p)
    for q in range(1, M):
        a = _a(n, q, p)
        d = _d(n, q, p, sq23pi, sqrt8)
        s = mpf_add(s, mpf_mul(a, d), prec)
        # On average, the terms decrease rapidly in magnitude.
        # Dynamically reducing the precision greatly improves
        # performance.
        p = bitcount(abs(to_int(d))) + 50
    return int(to_int(mpf_add(s, fhalf, prec)))


def _partition(seq, vector, m=None):
    """
    Return the partition of seq as specified by the partition vector.

    Examples
    ========

    >>> from sympy.utilities.iterables import _partition
    >>> _partition('abcde', [1, 0, 1, 2, 0])
    [['b', 'e'], ['a', 'c'], ['d']]

    Specifying the number of bins in the partition is optional:

    >>> _partition('abcde', [1, 0, 1, 2, 0], 3)
    [['b', 'e'], ['a', 'c'], ['d']]

    The output of _set_partitions can be passed as follows:

    >>> output = (3, [1, 0, 1, 2, 0])
    >>> _partition('abcde', *output)
    [['b', 'e'], ['a', 'c'], ['d']]

    See Also
    ========

    combinatorics.partitions.Partition.from_rgs

    """
    if m is None:
        m = max(vector) + 1
    elif isinstance(vector, int):  # entered as m, vector
        vector, m = m, vector
    p = [[] for i in range(m)]
    for i, v in enumerate(vector):
        p[v].append(seq[i])
    return p

