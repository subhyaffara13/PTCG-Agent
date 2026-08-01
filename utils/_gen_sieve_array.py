
def _gen_sieve_array(M, factor_base):
    """Sieve Stage of the Quadratic Sieve. For every prime in the factor_base
    that does not divide the coefficient `a` we add log_p over the sieve_array
    such that ``-M <= soln1 + i*p <=  M`` and ``-M <= soln2 + i*p <=  M`` where `i`
    is an integer. When p = 2 then log_p is only added using
    ``-M <= soln1 + i*p <=  M``.

    Parameters
    ==========

    M : sieve interval
    factor_base : factor_base primes
    """
    sieve_array = [0]*(2*M + 1)
    for factor in factor_base:
        if factor.soln1 is None: #The prime does not divides a
            continue
        for idx in range((M + factor.soln1) % factor.prime, 2*M, factor.prime):
            sieve_array[idx] += factor.log_p
        if factor.prime == 2:
            continue
        #if prime is 2 then sieve only with soln_1_p
        for idx in range((M + factor.soln2) % factor.prime, 2*M, factor.prime):
            sieve_array[idx] += factor.log_p
    return sieve_array

