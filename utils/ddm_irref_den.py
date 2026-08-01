
def ddm_irref_den(a, K):
    """a  <--  rref(a); return (den, pivots)

    Compute the fraction-free reduced row echelon form (RREF) of $a$. Modifies
    $a$ in place and returns a tuple containing the denominator of the RREF and
    a list of the pivot columns.

    Explanation
    ===========

    The algorithm used is the fraction-free version of Gauss-Jordan elimination
    described as FFGJ in [1]_. Here it is modified to handle zero or missing
    pivots and to avoid redundant arithmetic.

    The domain $K$ must support exact division (``K.exquo``) but does not need
    to be a field. This method is suitable for most exact rings and fields like
    :ref:`ZZ`, :ref:`QQ` and :ref:`QQ(a)`. In the case of :ref:`QQ` or
    :ref:`K(x)` it might be more efficient to clear denominators and use
    :ref:`ZZ` or :ref:`K[x]` instead.

    For inexact domains like :ref:`RR` and :ref:`CC` use ``ddm_irref`` instead.

    Examples
    ========

    >>> from sympy.polys.matrices.dense import ddm_irref_den
    >>> from sympy import ZZ, Matrix
    >>> M = [[ZZ(1), ZZ(2), ZZ(3)], [ZZ(4), ZZ(5), ZZ(6)]]
    >>> den, pivots = ddm_irref_den(M, ZZ)
    >>> M
    [[-3, 0, 3], [0, -3, -6]]
    >>> den
    -3
    >>> pivots
    [0, 1]
    >>> Matrix(M).rref()[0]
    Matrix([
    [1, 0, -1],
    [0, 1,  2]])

    See Also
    ========

    ddm_irref
        A version of this routine that uses field division.
    sdm_irref
        A sparse version of :func:`ddm_irref`.
    sdm_rref_den
        A sparse version of :func:`ddm_irref_den`.
    sympy.polys.matrices.domainmatrix.DomainMatrix.rref_den
        Higher level interface.

    References
    ==========

    .. [1] Fraction-free algorithms for linear and polynomial equations.
        George C. Nakos , Peter R. Turner , Robert M. Williams.
        https://dl.acm.org/doi/10.1145/271130.271133
    """
    #
    # A simpler presentation of this algorithm is given in [1]:
    #
    # Given an n x n matrix A and n x 1 matrix b:
    #
    #   for i in range(n):
    #       if i != 0:
    #           d = a[i-1][i-1]
    #       for j in range(n):
    #           if j == i:
    #               continue
    #           b[j] = a[i][i]*b[j] - a[j][i]*b[i]
    #           for k in range(n):
    #               a[j][k] = a[i][i]*a[j][k] - a[j][i]*a[i][k]
    #               if i != 0:
    #                   a[j][k] /= d
    #
    # Our version here is a bit more complicated because:
    #
    #  1. We use row-swaps to avoid zero pivots.
    #  2. We allow for some columns to be missing pivots.
    #  3. We avoid a lot of redundant arithmetic.
    #
    # TODO: Use a non-trivial pivoting strategy. Even just row swapping makes a
    # big difference to performance if e.g. the upper-left entry of the matrix
    # is a huge polynomial.

    # a is (m x n)
    m = len(a)
    if not m:
        return K.one, []
    n = len(a[0])

    d = None
    pivots = []
    no_pivots = []

    # i, j will be the row and column indices of the current pivot
    i = 0
    for j in range(n):
        # next pivot?
        aij = a[i][j]

        # swap rows if zero
        if not aij:
            for ip in range(i+1, m):
                aij = a[ip][j]
                # row-swap
                if aij:
                    a[i], a[ip] = a[ip], a[i]
                    break
            else:
                # go to next column
                no_pivots.append(j)
                continue

        # Now aij is the pivot and i,j are the row and column. We need to clear
        # the column above and below but we also need to keep track of the
        # denominator of the RREF which means also multiplying everything above
        # and to the left by the current pivot aij and dividing by d (which we
        # multiplied everything by in the previous iteration so this is an
        # exact division).
        #
        # First handle the upper left corner which is usually already diagonal
        # with all diagonal entries equal to the current denominator but there
        # can be other non-zero entries in any column that has no pivot.

        # Update previous pivots in the matrix
        if pivots:
            pivot_val = aij * a[0][pivots[0]]
            # Divide out the common factor
            if d is not None:
                pivot_val = K.exquo(pivot_val, d)

            # Could defer this until the end but it is pretty cheap and
            # helps when debugging.
            for ip, jp in enumerate(pivots):
                a[ip][jp] = pivot_val

        # Update columns without pivots
        for jnp in no_pivots:
            for ip in range(i):
                aijp = a[ip][jnp]
                if aijp:
                    aijp *= aij
                    if d is not None:
                        aijp = K.exquo(aijp, d)
                    a[ip][jnp] = aijp

        # Eliminate above, below and to the right as in ordinary division free
        # Gauss-Jordan elmination except also dividing out d from every entry.

        for jp, aj in enumerate(a):

            # Skip the current row
            if jp == i:
                continue

            # Eliminate to the right in all rows
            for kp in range(j+1, n):
                ajk = aij * aj[kp] - aj[j] * a[i][kp]
                if d is not None:
                    ajk = K.exquo(ajk, d)
                aj[kp] = ajk

            # Set to zero above and below the pivot
            aj[j] = K.zero

        # next row
        pivots.append(j)
        i += 1

        # no more rows left?
        if i >= m:
            break

        if not K.is_one(aij):
            d = aij
        else:
            d = None

    if not pivots:
        denom = K.one
    else:
        denom = a[0][pivots[0]]

    return denom, pivots

