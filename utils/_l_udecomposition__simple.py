
def _LUdecomposition_Simple(M, iszerofunc=_iszero, simpfunc=None,
        rankcheck=False):
    r"""Compute the PLU decomposition of the matrix.

    Parameters
    ==========

    rankcheck : bool, optional
        Determines if this function should detect the rank
        deficiency of the matrixis and should raise a
        ``ValueError``.

    iszerofunc : function, optional
        A function which determines if a given expression is zero.

        The function should be a callable that takes a single
        SymPy expression and returns a 3-valued boolean value
        ``True``, ``False``, or ``None``.

        It is internally used by the pivot searching algorithm.
        See the notes section for a more information about the
        pivot searching algorithm.

    simpfunc : function or None, optional
        A function that simplifies the input.

        If this is specified as a function, this function should be
        a callable that takes a single SymPy expression and returns
        an another SymPy expression that is algebraically
        equivalent.

        If ``None``, it indicates that the pivot search algorithm
        should not attempt to simplify any candidate pivots.

        It is internally used by the pivot searching algorithm.
        See the notes section for a more information about the
        pivot searching algorithm.

    Returns
    =======

    (lu, row_swaps) : (Matrix, list)
        If the original matrix is a $m, n$ matrix:

        *lu* is a $m, n$ matrix, which contains result of the
        decomposition in a compressed form. See the notes section
        to see how the matrix is compressed.

        *row_swaps* is a $m$-element list where each element is a
        pair of row exchange indices.

        ``A = (L*U).permute_backward(perm)``, and the row
        permutation matrix $P$ from the formula $P A = L U$ can be
        computed by ``P=eye(A.row).permute_forward(perm)``.

    Raises
    ======

    ValueError
        Raised if ``rankcheck=True`` and the matrix is found to
        be rank deficient during the computation.

    Notes
    =====

    About the PLU decomposition:

    PLU decomposition is a generalization of a LU decomposition
    which can be extended for rank-deficient matrices.

    It can further be generalized for non-square matrices, and this
    is the notation that SymPy is using.

    PLU decomposition is a decomposition of a $m, n$ matrix $A$ in
    the form of $P A = L U$ where

    * $L$ is a $m, m$ lower triangular matrix with unit diagonal
        entries.
    * $U$ is a $m, n$ upper triangular matrix.
    * $P$ is a $m, m$ permutation matrix.

    So, for a square matrix, the decomposition would look like:

    .. math::
        L = \begin{bmatrix}
        1 & 0 & 0 & \cdots & 0 \\
        L_{1, 0} & 1 & 0 & \cdots & 0 \\
        L_{2, 0} & L_{2, 1} & 1 & \cdots & 0 \\
        \vdots & \vdots & \vdots & \ddots & \vdots \\
        L_{n-1, 0} & L_{n-1, 1} & L_{n-1, 2} & \cdots & 1
        \end{bmatrix}

    .. math::
        U = \begin{bmatrix}
        U_{0, 0} & U_{0, 1} & U_{0, 2} & \cdots & U_{0, n-1} \\
        0 & U_{1, 1} & U_{1, 2} & \cdots & U_{1, n-1} \\
        0 & 0 & U_{2, 2} & \cdots & U_{2, n-1} \\
        \vdots & \vdots & \vdots & \ddots & \vdots \\
        0 & 0 & 0 & \cdots & U_{n-1, n-1}
        \end{bmatrix}

    And for a matrix with more rows than the columns,
    the decomposition would look like:

    .. math::
        L = \begin{bmatrix}
        1 & 0 & 0 & \cdots & 0 & 0 & \cdots & 0 \\
        L_{1, 0} & 1 & 0 & \cdots & 0 & 0 & \cdots & 0 \\
        L_{2, 0} & L_{2, 1} & 1 & \cdots & 0 & 0 & \cdots & 0 \\
        \vdots & \vdots & \vdots & \ddots & \vdots & \vdots & \ddots
        & \vdots \\
        L_{n-1, 0} & L_{n-1, 1} & L_{n-1, 2} & \cdots & 1 & 0
        & \cdots & 0 \\
        L_{n, 0} & L_{n, 1} & L_{n, 2} & \cdots & L_{n, n-1} & 1
        & \cdots & 0 \\
        \vdots & \vdots & \vdots & \ddots & \vdots & \vdots
        & \ddots & \vdots \\
        L_{m-1, 0} & L_{m-1, 1} & L_{m-1, 2} & \cdots & L_{m-1, n-1}
        & 0 & \cdots & 1 \\
        \end{bmatrix}

    .. math::
        U = \begin{bmatrix}
        U_{0, 0} & U_{0, 1} & U_{0, 2} & \cdots & U_{0, n-1} \\
        0 & U_{1, 1} & U_{1, 2} & \cdots & U_{1, n-1} \\
        0 & 0 & U_{2, 2} & \cdots & U_{2, n-1} \\
        \vdots & \vdots & \vdots & \ddots & \vdots \\
        0 & 0 & 0 & \cdots & U_{n-1, n-1} \\
        0 & 0 & 0 & \cdots & 0 \\
        \vdots & \vdots & \vdots & \ddots & \vdots \\
        0 & 0 & 0 & \cdots & 0
        \end{bmatrix}

    Finally, for a matrix with more columns than the rows, the
    decomposition would look like:

    .. math::
        L = \begin{bmatrix}
        1 & 0 & 0 & \cdots & 0 \\
        L_{1, 0} & 1 & 0 & \cdots & 0 \\
        L_{2, 0} & L_{2, 1} & 1 & \cdots & 0 \\
        \vdots & \vdots & \vdots & \ddots & \vdots \\
        L_{m-1, 0} & L_{m-1, 1} & L_{m-1, 2} & \cdots & 1
        \end{bmatrix}

    .. math::
        U = \begin{bmatrix}
        U_{0, 0} & U_{0, 1} & U_{0, 2} & \cdots & U_{0, m-1}
        & \cdots & U_{0, n-1} \\
        0 & U_{1, 1} & U_{1, 2} & \cdots & U_{1, m-1}
        & \cdots & U_{1, n-1} \\
        0 & 0 & U_{2, 2} & \cdots & U_{2, m-1}
        & \cdots & U_{2, n-1} \\
        \vdots & \vdots & \vdots & \ddots & \vdots
        & \cdots & \vdots \\
        0 & 0 & 0 & \cdots & U_{m-1, m-1}
        & \cdots & U_{m-1, n-1} \\
        \end{bmatrix}

    About the compressed LU storage:

    The results of the decomposition are often stored in compressed
    forms rather than returning $L$ and $U$ matrices individually.

    It may be less intiuitive, but it is commonly used for a lot of
    numeric libraries because of the efficiency.

    The storage matrix is defined as following for this specific
    method:

    * The subdiagonal elements of $L$ are stored in the subdiagonal
        portion of $LU$, that is $LU_{i, j} = L_{i, j}$ whenever
        $i > j$.
    * The elements on the diagonal of $L$ are all 1, and are not
        explicitly stored.
    * $U$ is stored in the upper triangular portion of $LU$, that is
        $LU_{i, j} = U_{i, j}$ whenever $i <= j$.
    * For a case of $m > n$, the right side of the $L$ matrix is
        trivial to store.
    * For a case of $m < n$, the below side of the $U$ matrix is
        trivial to store.

    So, for a square matrix, the compressed output matrix would be:

    .. math::
        LU = \begin{bmatrix}
        U_{0, 0} & U_{0, 1} & U_{0, 2} & \cdots & U_{0, n-1} \\
        L_{1, 0} & U_{1, 1} & U_{1, 2} & \cdots & U_{1, n-1} \\
        L_{2, 0} & L_{2, 1} & U_{2, 2} & \cdots & U_{2, n-1} \\
        \vdots & \vdots & \vdots & \ddots & \vdots \\
        L_{n-1, 0} & L_{n-1, 1} & L_{n-1, 2} & \cdots & U_{n-1, n-1}
        \end{bmatrix}

    For a matrix with more rows than the columns, the compressed
    output matrix would be:

    .. math::
        LU = \begin{bmatrix}
        U_{0, 0} & U_{0, 1} & U_{0, 2} & \cdots & U_{0, n-1} \\
        L_{1, 0} & U_{1, 1} & U_{1, 2} & \cdots & U_{1, n-1} \\
        L_{2, 0} & L_{2, 1} & U_{2, 2} & \cdots & U_{2, n-1} \\
        \vdots & \vdots & \vdots & \ddots & \vdots \\
        L_{n-1, 0} & L_{n-1, 1} & L_{n-1, 2} & \cdots
        & U_{n-1, n-1} \\
        \vdots & \vdots & \vdots & \ddots & \vdots \\
        L_{m-1, 0} & L_{m-1, 1} & L_{m-1, 2} & \cdots
        & L_{m-1, n-1} \\
        \end{bmatrix}

    For a matrix with more columns than the rows, the compressed
    output matrix would be:

    .. math::
        LU = \begin{bmatrix}
        U_{0, 0} & U_{0, 1} & U_{0, 2} & \cdots & U_{0, m-1}
        & \cdots & U_{0, n-1} \\
        L_{1, 0} & U_{1, 1} & U_{1, 2} & \cdots & U_{1, m-1}
        & \cdots & U_{1, n-1} \\
        L_{2, 0} & L_{2, 1} & U_{2, 2} & \cdots & U_{2, m-1}
        & \cdots & U_{2, n-1} \\
        \vdots & \vdots & \vdots & \ddots & \vdots
        & \cdots & \vdots \\
        L_{m-1, 0} & L_{m-1, 1} & L_{m-1, 2} & \cdots & U_{m-1, m-1}
        & \cdots & U_{m-1, n-1} \\
        \end{bmatrix}

    About the pivot searching algorithm:

    When a matrix contains symbolic entries, the pivot search algorithm
    differs from the case where every entry can be categorized as zero or
    nonzero.
    The algorithm searches column by column through the submatrix whose
    top left entry coincides with the pivot position.
    If it exists, the pivot is the first entry in the current search
    column that iszerofunc guarantees is nonzero.
    If no such candidate exists, then each candidate pivot is simplified
    if simpfunc is not None.
    The search is repeated, with the difference that a candidate may be
    the pivot if ``iszerofunc()`` cannot guarantee that it is nonzero.
    In the second search the pivot is the first candidate that
    iszerofunc can guarantee is nonzero.
    If no such candidate exists, then the pivot is the first candidate
    for which iszerofunc returns None.
    If no such candidate exists, then the search is repeated in the next
    column to the right.
    The pivot search algorithm differs from the one in ``rref()``, which
    relies on ``_find_reasonable_pivot()``.
    Future versions of ``LUdecomposition_simple()`` may use
    ``_find_reasonable_pivot()``.

    See Also
    ========

    sympy.matrices.matrixbase.MatrixBase.LUdecomposition
    LUdecompositionFF
    LUsolve
    """

    if rankcheck:
        # https://github.com/sympy/sympy/issues/9796
        pass

    if S.Zero in M.shape:
        # Define LU decomposition of a matrix with no entries as a matrix
        # of the same dimensions with all zero entries.
        return M.zeros(M.rows, M.cols), []

    dps       = _get_intermediate_simp()
    lu        = M.as_mutable()
    row_swaps = []

    pivot_col = 0

    for pivot_row in range(0, lu.rows - 1):
        # Search for pivot. Prefer entry that iszeropivot determines
        # is nonzero, over entry that iszeropivot cannot guarantee
        # is  zero.
        # XXX ``_find_reasonable_pivot`` uses slow zero testing. Blocked by bug #10279
        # Future versions of LUdecomposition_simple can pass iszerofunc and simpfunc
        # to _find_reasonable_pivot().
        # In pass 3 of _find_reasonable_pivot(), the predicate in ``if x.equals(S.Zero):``
        # calls sympy.simplify(), and not the simplification function passed in via
        # the keyword argument simpfunc.
        iszeropivot = True

        while pivot_col != M.cols and iszeropivot:
            sub_col = (lu[r, pivot_col] for r in range(pivot_row, M.rows))

            pivot_row_offset, pivot_value, is_assumed_non_zero, ind_simplified_pairs =\
                _find_reasonable_pivot_naive(sub_col, iszerofunc, simpfunc)

            iszeropivot = pivot_value is None

            if iszeropivot:
                # All candidate pivots in this column are zero.
                # Proceed to next column.
                pivot_col += 1

        if rankcheck and pivot_col != pivot_row:
            # All entries including and below the pivot position are
            # zero, which indicates that the rank of the matrix is
            # strictly less than min(num rows, num cols)
            # Mimic behavior of previous implementation, by throwing a
            # ValueError.
            raise ValueError("Rank of matrix is strictly less than"
                                " number of rows or columns."
                                " Pass keyword argument"
                                " rankcheck=False to compute"
                                " the LU decomposition of this matrix.")

        candidate_pivot_row = None if pivot_row_offset is None else pivot_row + pivot_row_offset

        if candidate_pivot_row is None and iszeropivot:
            # If candidate_pivot_row is None and iszeropivot is True
            # after pivot search has completed, then the submatrix
            # below and to the right of (pivot_row, pivot_col) is
            # all zeros, indicating that Gaussian elimination is
            # complete.
            return lu, row_swaps

        # Update entries simplified during pivot search.
        for offset, val in ind_simplified_pairs:
            lu[pivot_row + offset, pivot_col] = val

        if pivot_row != candidate_pivot_row:
            # Row swap book keeping:
            # Record which rows were swapped.
            # Update stored portion of L factor by multiplying L on the
            # left and right with the current permutation.
            # Swap rows of U.
            row_swaps.append([pivot_row, candidate_pivot_row])

            # Update L.
            lu[pivot_row, 0:pivot_row], lu[candidate_pivot_row, 0:pivot_row] = \
                lu[candidate_pivot_row, 0:pivot_row], lu[pivot_row, 0:pivot_row]

            # Swap pivot row of U with candidate pivot row.
            lu[pivot_row, pivot_col:lu.cols], lu[candidate_pivot_row, pivot_col:lu.cols] = \
                lu[candidate_pivot_row, pivot_col:lu.cols], lu[pivot_row, pivot_col:lu.cols]

        # Introduce zeros below the pivot by adding a multiple of the
        # pivot row to a row under it, and store the result in the
        # row under it.
        # Only entries in the target row whose index is greater than
        # start_col may be nonzero.
        start_col = pivot_col + 1

        for row in range(pivot_row + 1, lu.rows):
            # Store factors of L in the subcolumn below
            # (pivot_row, pivot_row).
            lu[row, pivot_row] = \
                dps(lu[row, pivot_col]/lu[pivot_row, pivot_col])

            # Form the linear combination of the pivot row and the current
            # row below the pivot row that zeros the entries below the pivot.
            # Employing slicing instead of a loop here raises
            # NotImplementedError: Cannot add Zero to MutableSparseMatrix
            # in sympy/matrices/tests/test_sparse.py.
            # c = pivot_row + 1 if pivot_row == pivot_col else pivot_col
            for c in range(start_col, lu.cols):
                lu[row, c] = dps(lu[row, c] - lu[row, pivot_row]*lu[pivot_row, c])

        if pivot_row != pivot_col:
            # matrix rank < min(num rows, num cols),
            # so factors of L are not stored directly below the pivot.
            # These entries are zero by construction, so don't bother
            # computing them.
            for row in range(pivot_row + 1, lu.rows):
                lu[row, pivot_col] = M.zero

        pivot_col += 1

        if pivot_col == lu.cols:
            # All candidate pivots are zero implies that Gaussian
            # elimination is complete.
            return lu, row_swaps

    if rankcheck:
        if iszerofunc(
                lu[Min(lu.rows, lu.cols) - 1, Min(lu.rows, lu.cols) - 1]):
            raise ValueError("Rank of matrix is strictly less than"
                                " number of rows or columns."
                                " Pass keyword argument"
                                " rankcheck=False to compute"
                                " the LU decomposition of this matrix.")

    return lu, row_swaps

