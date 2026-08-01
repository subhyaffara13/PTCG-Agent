
def _can_do_sum_of_squares(n, k):
    """Return True if n can be written as the sum of k squares,
    False if it cannot, or 1 if ``k == 2`` and ``n`` is prime (in which
    case it *can* be written as a sum of two squares). A False
    is returned only if it cannot be written as ``k``-squares, even
    if 0s are allowed.
    """
    if k < 1:
        return False
    if n < 0:
        return False
    if n == 0:
        return True
    if k == 1:
        return is_square(n)
    if k == 2:
        if n in (1, 2):
            return True
        if isprime(n):
            if n % 4 == 1:
                return 1  # signal that it was prime
            return False
        # n is a composite number
        # we can proceed iff no prime factor in the form 4*k + 3
        # has an odd multiplicity
        return all(p % 4 !=3 or m % 2 == 0 for p, m in factorint(n).items())
    if k == 3:
        return remove(n, 4)[0] % 8 != 7
    # every number can be written as a sum of 4 squares; for k > 4 partitions
    # can be 0
    return True

