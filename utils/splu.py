
def splu(A, permc_spec=None, diag_pivot_thresh=None,
         relax=None, panel_size=None, options=None):
    """
    Compute the LU decomposition of a sparse, square matrix.

    Parameters
    ----------
    A : sparse array or matrix
        Sparse array to factorize. Most efficient when provided in CSC
        format. Other formats will be converted to CSC before factorization.
    permc_spec : str, optional
        How to permute the columns of the matrix for sparsity preservation.
        (default: 'COLAMD')

        - ``NATURAL``: natural ordering.
        - ``MMD_ATA``: minimum degree ordering on the structure of A^T A.
        - ``MMD_AT_PLUS_A``: minimum degree ordering on the structure of A^T+A.
        - ``COLAMD``: approximate minimum degree column ordering

    diag_pivot_thresh : float, optional
        Threshold used for a diagonal entry to be an acceptable pivot.
        See SuperLU user's guide for details [1]_
    relax : int, optional
        Expert option for customizing the degree of relaxing supernodes.
        See SuperLU user's guide for details [1]_
    panel_size : int, optional
        Expert option for customizing the panel size.
        See SuperLU user's guide for details [1]_
    options : dict, optional
        Dictionary containing additional expert options to SuperLU.
        See SuperLU user guide [1]_ (section 2.4 on the 'Options' argument)
        for more details. For example, you can specify
        ``options=dict(Equil=False, IterRefine='SINGLE'))``
        to turn equilibration off and perform a single iterative refinement.

    Returns
    -------
    invA : scipy.sparse.linalg.SuperLU
        Object, which has a ``solve`` method.

    See Also
    --------
    spilu : incomplete LU decomposition

    Notes
    -----
    When a real array is factorized and the returned SuperLU object's ``solve()``
    method is used with complex arguments an error is generated. Instead, cast the
    initial array to complex and then factorize.

    This function uses the SuperLU library.

    References
    ----------
    .. [1] SuperLU https://portal.nersc.gov/project/sparse/superlu/

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import csc_array
    >>> from scipy.sparse.linalg import splu
    >>> A = csc_array([[1., 0., 0.], [5., 0., 2.], [0., -1., 0.]], dtype=float)
    >>> B = splu(A)
    >>> x = np.array([1., 2., 3.], dtype=float)
    >>> B.solve(x)
    array([ 1. , -3. , -1.5])
    >>> A.dot(B.solve(x))
    array([ 1.,  2.,  3.])
    >>> B.solve(A.dot(x))
    array([ 1.,  2.,  3.])
    """

    if is_pydata_spmatrix(A):
        A_cls = type(A)
        def csc_construct_func(*a, cls=A_cls):
            return cls.from_scipy_sparse(csc_array(*a))
        A = A.to_scipy_sparse().tocsc()
    else:
        csc_construct_func = csc_array

    if not (issparse(A) and A.format == "csc"):
        A = csc_array(A)
        warn('splu converted its input to CSC format',
             SparseEfficiencyWarning, stacklevel=2)

    # sum duplicates for non-canonical format
    A.sum_duplicates()
    A = A._asfptype()  # upcast to a floating point format

    M, N = A.shape
    if (M != N):
        raise ValueError("can only factor square matrices")  # is this true?

    indices, indptr = safely_cast_index_arrays(A, np.intc, "SuperLU")

    _options = dict(DiagPivotThresh=diag_pivot_thresh, ColPerm=permc_spec,
                    PanelSize=panel_size, Relax=relax)
    if options is not None:
        _options.update(options)

    # Ensure that no column permutations are applied
    if (_options["ColPerm"] == "NATURAL"):
        _options["SymmetricMode"] = True

    return _superlu.gstrf(N, A.nnz, A.data, indices, indptr,
                          csc_construct_func=csc_construct_func,
                          ilu=False, options=_options)

