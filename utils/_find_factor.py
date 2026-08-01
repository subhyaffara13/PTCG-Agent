
def _find_factor(N, smooth_relations, col):
    """ Finds proper factor of N using fast gaussian reduction for modulo 2 matrix.

    Parameters
    ==========

    N : Number to be factored
    smooth_relations : Smooth relations vectors matrix
    col : Number of columns in the matrix

    Reference
    ==========

    .. [1] A fast algorithm for gaussian elimination over GF(2) and
    its implementation on the GAPP. Cetin K.Koc, Sarath N.Arachchige
    """
    matrix = [s_relation[2] for s_relation in smooth_relations]
    row = len(matrix)
    mark = [False] * row
    for pos in range(col):
        m = 1 << pos
        for i in range(row):
            if p := matrix[i] & m:
                add_col = p ^ matrix[i]
                matrix[i] = m
                mark[i] = True
                for j in range(i + 1, row):
                    if matrix[j] & m:
                        matrix[j] ^= add_col
                break

    for m, mat, rel in zip(mark, matrix, smooth_relations):
        if m:
            continue
        u, v = rel[0], rel[1]
        for m1, mat1, rel1 in zip(mark, matrix, smooth_relations):
            if m1 and mat & mat1:
                u *= rel1[0]
                v *= rel1[1]
        # assert is_square(v)
        v = isqrt(v)
        if 1 < (g := gcd(u - v, N)) < N:
            yield g

