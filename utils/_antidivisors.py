
def _antidivisors(n):
    """Helper function for antidivisors which generates the antidivisors.

    Parameters
    ==========

    n : int
        a nonnegative integer

    """
    if n <= 2:
        return
    for d in _divisors(n):
        y = 2*d
        if n > y and n % y:
            yield y
    for d in _divisors(2*n-1):
        if n > d >= 2 and n % d:
            yield d
    for d in _divisors(2*n+1):
        if n > d >= 2 and n % d:
            yield d

