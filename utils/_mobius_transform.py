
def _mobius_transform(seq, sgn, subset):
    r"""Utility function for performing Mobius Transform using
    Yate's Dynamic Programming method"""

    if not iterable(seq):
        raise TypeError("Expected a sequence of coefficients")

    a = [sympify(arg) for arg in seq]

    n = len(a)
    if n < 2:
        return a

    if n&(n - 1):
        n = 2**n.bit_length()

    a += [S.Zero]*(n - len(a))

    if subset:
        i = 1
        while i < n:
            for j in range(n):
                if j & i:
                    a[j] += sgn*a[j ^ i]
            i *= 2

    else:
        i = 1
        while i < n:
            for j in range(n):
                if j & i:
                    continue
                a[j] += sgn*a[j ^ i]
            i *= 2

    return a

