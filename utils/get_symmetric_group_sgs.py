
def get_symmetric_group_sgs(n, antisym=False):
    """
    Return base, gens of the minimal BSGS for (anti)symmetric tensor

    Parameters
    ==========

    n : rank of the tensor
    antisym : bool
        ``antisym = False`` symmetric tensor
        ``antisym = True``  antisymmetric tensor

    Examples
    ========

    >>> from sympy.combinatorics.tensor_can import get_symmetric_group_sgs
    >>> get_symmetric_group_sgs(3)
    ([0, 1], [(4)(0 1), (4)(1 2)])
    """
    if n == 1:
        return [], [_af_new(list(range(3)))]
    gens = [Permutation(n - 1)(i, i + 1)._array_form for i in range(n - 1)]
    if antisym == 0:
        gens = [x + [n, n + 1] for x in gens]
    else:
        gens = [x + [n + 1, n] for x in gens]
    base = list(range(n - 1))
    return base, [_af_new(h) for h in gens]

