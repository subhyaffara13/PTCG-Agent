
def _nth_prime_bounds(n):
    """Bounds for the nth prime (counting from 1): lb < p_n < ub."""
    # At and above 688,383, the lb/ub spread is under 0.003 * p_n.

    if n < 1:
        raise ValueError

    if n < 6:
        return (n, 2.25 * n)

    # https://en.wikipedia.org/wiki/Prime-counting_function#Inequalities
    upper_bound = n * log(n * log(n))
    lower_bound = upper_bound - n
    if n >= 688_383:
        upper_bound -= n * (1.0 - (log(log(n)) - 2.0) / log(n))

    return lower_bound, upper_bound

