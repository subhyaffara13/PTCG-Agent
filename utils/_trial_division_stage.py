
def _trial_division_stage(N, M, factor_base, sieve_array, sieve_poly, partial_relations, ERROR_TERM):
    """Trial division stage. Here we trial divide the values generetated
    by sieve_poly in the sieve interval and if it is a smooth number then
    it is stored in `smooth_relations`. Moreover, if we find two partial relations
    with same large prime then they are combined to form a smooth relation.
    First we iterate over sieve array and look for values which are greater
    than accumulated_val, as these values have a high chance of being smooth
    number. Then using these values we find smooth relations.
    In general, let ``t**2 = u*p modN`` and ``r**2 = v*p modN`` be two partial relations
    with the same large prime p. Then they can be combined ``(t*r/p)**2 = u*v modN``
    to form a smooth relation.

    Parameters
    ==========

    N : Number to be factored
    M : sieve interval
    factor_base : factor_base primes
    sieve_array : stores log_p values
    sieve_poly : polynomial from which we find smooth relations
    partial_relations : stores partial relations with one large prime
    ERROR_TERM : error term for accumulated_val
    """
    accumulated_val = (log(M) + log(N)/2 - ERROR_TERM) * 2**10
    smooth_relations = []
    proper_factor = set()
    partial_relation_upper_bound = 128*factor_base[-1].prime
    for x, val in enumerate(sieve_array, -M):
        if val < accumulated_val:
            continue
        v = sieve_poly.eval_v(x)
        vec, num = _check_smoothness(v, factor_base)
        if num == 1:
            smooth_relations.append((sieve_poly.eval_u(x), v, vec))
        elif num < partial_relation_upper_bound and isprime(num):
            if N % num == 0:
                proper_factor.add(num)
                continue
            u = sieve_poly.eval_u(x)
            if num in partial_relations:
                u_prev, v_prev, vec_prev = partial_relations.pop(num)
                u = u*u_prev*invert(num, N) % N
                v = v*v_prev // num**2
                vec ^= vec_prev
                smooth_relations.append((u, v, vec))
            else:
                partial_relations[num] = (u, v, vec)
    return smooth_relations, proper_factor

