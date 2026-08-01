
def qs_factor(N, prime_bound, M, ERROR_TERM=25, seed=1234):
    """ Performs factorization using Self-Initializing Quadratic Sieve.

    Parameters
    ==========

    N : Number to be Factored
    prime_bound : upper bound for primes in the factor base
    M : Sieve Interval
    ERROR_TERM : Error term for checking smoothness
    seed : seed of random number generator

    Returns
    =======

    dict[int, int] : Factors of N.
                     Returns ``{N: 1}`` if factorization fails.
                     Note that the key is not always a prime number.

    Examples
    ========

    >>> from sympy.ntheory import qs_factor
    >>> qs_factor(1009 * 100003, 2000, 10000)
    {1009: 1, 100003: 1}

    See Also
    ========

    qs

    """
    if N < 2:
        raise ValueError("N should be greater than 1")
    factors = {}
    smooth_relations = []
    partial_relations = {}
    # Eliminate the possibility of even numbers,
    # prime numbers, and perfect powers.
    if N % 2 == 0:
        e = 1
        N //= 2
        while N % 2 == 0:
            N //= 2
            e += 1
        factors[2] = e
    if isprime(N):
        factors[N] = 1
        return factors
    if result := _perfect_power(N, 3):
        n, e = result
        factors[n] = e
        return factors
    N_copy = N
    randint = _randint(seed)
    idx_1000, idx_5000, factor_base = _generate_factor_base(prime_bound, N)
    threshold = len(factor_base) * 105//100
    for g in _generate_polynomial(N, M, factor_base, idx_1000, idx_5000, randint):
        sieve_array = _gen_sieve_array(M, factor_base)
        s_rel, p_f = _trial_division_stage(N, M, factor_base, sieve_array, g, partial_relations, ERROR_TERM)
        smooth_relations += s_rel
        for p in p_f:
            if N_copy % p:
                continue
            e = 1
            N_copy //= p
            while N_copy % p == 0:
                N_copy //= p
                e += 1
            factors[p] = e
        if threshold <= len(smooth_relations):
            break

    for factor in _find_factor(N, smooth_relations, len(factor_base) + 1):
        if N_copy % factor == 0:
            e = 1
            N_copy //= factor
            while N_copy % factor == 0:
                N_copy //= factor
                e += 1
            factors[factor] = e
            if N_copy == 1 or isprime(N_copy):
                break
    if N_copy != 1:
        factors[N_copy] = 1
    return factors

