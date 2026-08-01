
def mpf_gamma_int(n, prec, rnd=round_fast):
    if n < SMALL_FACTORIAL_CACHE_SIZE:
        return mpf_pos(small_factorial_cache[n-1], prec, rnd)
    return mpf_gamma(from_int(n), prec, rnd)

