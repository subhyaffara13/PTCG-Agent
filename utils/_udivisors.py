
def _udivisors(n):
    """Helper function for udivisors which generates the unitary divisors.

    Parameters
    ==========

    n : int
        a nonnegative integer

    """
    if n <= 1:
        if n == 1:
            yield 1
        return

    factorpows = [p**e for p, e in factorint(n).items()]
    # We want to calculate
    # yield from (math.prod(s) for s in powersets(factorpows))
    for i in range(2**len(factorpows)):
        d = 1
        for k in range(i.bit_length()):
            if i & 1:
                d *= factorpows[k]
            i >>= 1
        yield d

