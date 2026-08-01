
def _af_pow(a, n):
    """
    Routine for finding powers of a permutation.

    Examples
    ========

    >>> from sympy.combinatorics import Permutation
    >>> from sympy.combinatorics.permutations import _af_pow
    >>> p = Permutation([2, 0, 3, 1])
    >>> p.order()
    4
    >>> _af_pow(p._array_form, 4)
    [0, 1, 2, 3]
    """
    if n == 0:
        return list(range(len(a)))
    if n < 0:
        return _af_pow(_af_invert(a), -n)
    if n == 1:
        return a[:]
    elif n == 2:
        b = [a[i] for i in a]
    elif n == 3:
        b = [a[a[i]] for i in a]
    elif n == 4:
        b = [a[a[a[i]]] for i in a]
    else:
        # use binary multiplication
        b = list(range(len(a)))
        while 1:
            if n & 1:
                b = [b[i] for i in a]
                n -= 1
                if not n:
                    break
            if n % 4 == 0:
                a = [a[a[a[i]]] for i in a]
                n = n // 4
            elif n % 2 == 0:
                a = [a[i] for i in a]
                n = n // 2
    return b

