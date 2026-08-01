
def det_perm(M):
    """
    Return the determinant of *M* by using permutations to select factors.

    Explanation
    ===========

    For sizes larger than 8 the number of permutations becomes prohibitively
    large, or if there are no symbols in the matrix, it is better to use the
    standard determinant routines (e.g., ``M.det()``.)

    See Also
    ========

    det_minor
    det_quick

    """
    args = []
    s = True
    n = M.rows
    list_ = M.flat()
    for perm in generate_bell(n):
        fac = []
        idx = 0
        for j in perm:
            fac.append(list_[idx + j])
            idx += n
        term = Mul(*fac) # disaster with unevaluated Mul -- takes forever for n=7
        args.append(term if s else -term)
        s = not s
    return Add(*args)

