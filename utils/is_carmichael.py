
def is_carmichael(n):
    """ Returns True if the numbers `n` is Carmichael number, else False.

    Parameters
    ==========

    n : Integer

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Carmichael_number
    .. [2] https://oeis.org/A002997

    """
    if n < 561:
        return False
    return n % 2 and not isprime(n) and \
           all(e == 1 and (n - 1) % (p - 1) == 0 for p, e in factorint(n).items())

