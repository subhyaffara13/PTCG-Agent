
def _discrete_log_is_smooth(n: int, factorbase: list):
    """Try to factor n with respect to a given factorbase.
    Upon success a list of exponents with respect to the factorbase is returned.
    Otherwise None."""
    factors = [0]*len(factorbase)
    for i, p in enumerate(factorbase):
        while n % p == 0: # divide by p as many times as possible
            factors[i] += 1
            n = n // p
    if n != 1:
        return None # the number factors if at the end nothing is left
    return factors

