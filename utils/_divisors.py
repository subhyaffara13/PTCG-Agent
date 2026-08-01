
def _divisors(n, proper=False):
    """Helper function for divisors which generates the divisors.

    Parameters
    ==========

    n : int
        a nonnegative integer
    proper: bool
        If `True`, returns the generator that outputs only the proper divisor (i.e., excluding n).

    """
    if n <= 1:
        if not proper and n:
            yield 1
        return

    factordict = factorint(n)
    ps = sorted(factordict.keys())

    def rec_gen(n=0):
        if n == len(ps):
            yield 1
        else:
            pows = [1]
            for _ in range(factordict[ps[n]]):
                pows.append(pows[-1] * ps[n])
            yield from (p * q for q in rec_gen(n + 1) for p in pows)

    if proper:
        yield from (p for p in rec_gen() if p != n)
    else:
        yield from rec_gen()

