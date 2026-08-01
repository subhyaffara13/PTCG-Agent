
def spsolve(A, b, permc_spec=None, use_umfpack=True):
    """Solve the sparse linear system Ax=b, where b may be a vector or a matrix.

    Parameters
    ----------
    A : ndarray or sparse array or matrix
        The square matrix A will be converted into CSC or CSR form
    b : ndarray or sparse array or matrix
        The matrix or vector representing the right hand side of the equation.
        If a vector, b.shape must be (n,) or (n, 1).
    permc_spec : str, optional
        How to permute the columns of the matrix for sparsity preservation.
        (default: 'COLAMD')

        - ``NATURAL``: natural ordering.
        - ``MMD_ATA``: minimum degree ordering on the structure of A^T A.
        - ``MMD_AT_PLUS_A``: minimum degree ordering on the structure of A^T+A.
        - ``COLAMD``: approximate minimum degree column ordering [1]_, [2]_.

    use_umfpack : bool, optional
        if True (default) then use UMFPACK for the solution [3]_, [4]_, [5]_,
        [6]_ . This is only referenced if b is a vector and
        ``scikits.umfpack`` is installed.

    Returns
    -------
    x : ndarray or sparse array or matrix
        the solution of the sparse linear equation.
        If b is a vector, then x is a vector of size A.shape[1]
        If b is a matrix, then x is a matrix of size (A.shape[1], b.shape[1])

    Notes
    -----
    For solving the matrix expression AX = B, this solver assumes the resulting
    matrix X is sparse, as is often the case for very sparse inputs.  If the
    resulting X is dense, the construction of this sparse result will be
    relatively expensive.  In that case, consider converting A to a dense
    matrix and using scipy.linalg.solve or its variants.

    References
    ----------
    .. [1] T. A. Davis, J. R. Gilbert, S. Larimore, E. Ng, Algorithm 836:
           COLAMD, an approximate column minimum degree ordering algorithm,
           ACM Trans. on Mathematical Software, 30(3), 2004, pp. 377--380.
           :doi:`10.1145/1024074.1024080`

    .. [2] T. A. Davis, J. R. Gilbert, S. Larimore, E. Ng, A column approximate
           minimum degree ordering algorithm, ACM Trans. on Mathematical
           Software, 30(3), 2004, pp. 353--376. :doi:`10.1145/1024074.1024079`

    .. [3] T. A. Davis, Algorithm 832:  UMFPACK - an unsymmetric-pattern
           multifrontal method with a column pre-ordering strategy, ACM
           Trans. on Mathematical Software, 30(2), 2004, pp. 196--199.
           :doi:`10.1145/992200.992206`.

    .. [4] T. A. Davis, A column pre-ordering strategy for the
           unsymmetric-pattern multifrontal method, ACM Trans.
           on Mathematical Software, 30(2), 2004, pp. 165--195.
           :doi:`10.1145/992200.992205`.

    .. [5] T. A. Davis and I. S. Duff, A combined unifrontal/multifrontal
           method for unsymmetric sparse matrices, ACM Trans. on
           Mathematical Software, 25(1), 1999, pp. 1--19.
           :doi:`10.1145/305658.287640`.

    .. [6] T. A. Davis and I. S. Duff, An unsymmetric-pattern multifrontal
           method for sparse LU factorization, SIAM J. Matrix Analysis and
           Computations, 18(1), 1997, pp. 140--158.
           :doi:`10.1137/S0895479894246905T`.


    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import csc_array
    >>> from scipy.sparse.linalg import spsolve
    >>> A = csc_array([[3, 2, 0], [1, -1, 0], [0, 5, 1]], dtype=float)
    >>> B = csc_array([[2, 0], [-1, 0], [2, 0]], dtype=float)
    >>> x = spsolve(A, B)
    >>> np.allclose(A.dot(x).toarray(), B.toarray())
    True
    """
    is_pydata_sparse = is_pydata_spmatrix(b)
    pydata_sparse_cls = b.__class__ if is_pydata_sparse else None
    A = convert_pydata_sparse_to_scipy(A)
    b = convert_pydata_sparse_to_scipy(b)

    if not (issparse(A) and A.format in ("csc", "csr")):
        A = csc_array(A)
        warn('spsolve requires A be CSC or CSR matrix format',
             SparseEfficiencyWarning, stacklevel=2)

    # b is a vector only if b have shape (n,) or (n, 1)
    b_is_sparse = issparse(b)
    if not b_is_sparse:
        b = asarray(b)
    b_is_vector = ((b.ndim == 1) or (b.ndim == 2 and b.shape[1] == 1))

    # sum duplicates for non-canonical format
    A.sum_duplicates()
    A = A._asfptype()  # upcast to a floating point format
    result_dtype = np.promote_types(A.dtype, b.dtype)
    if A.dtype != result_dtype:
        A = A.astype(result_dtype)
    if b.dtype != result_dtype:
        b = b.astype(result_dtype)

    # validate input shapes
    M, N = A.shape
    if (M != N):
        raise ValueError(f"matrix must be square (has shape {(M, N)})")

    if M != b.shape[0]:
        raise ValueError(f"matrix - rhs dimension mismatch ({A.shape} - {b.shape[0]})")

    if not hasattr(useUmfpack, 'u'):
        useUmfpack.u = not noScikit

    use_umfpack = use_umfpack and useUmfpack.u

    if b_is_vector and use_umfpack:
        if b_is_sparse:
            b_vec = b.toarray()
        else:
            b_vec = b
        b_vec = asarray(b_vec, dtype=A.dtype).ravel()

        if noScikit:
            raise RuntimeError('Scikits.umfpack not installed.')

        if A.dtype.char not in 'dD':
            raise ValueError("convert matrix data to double, please, using"
                  " .astype(), or set linsolve.useUmfpack.u = False")

        umf_family, A = _get_umf_family(A)
        umf = umfpack.UmfpackContext(umf_family)
        x = umf.linsolve(umfpack.UMFPACK_A, A, b_vec,
                         autoTranspose=True)
    else:
        if b_is_vector and b_is_sparse:
            b = b.toarray()
            b_is_sparse = False

        if not b_is_sparse:
            if A.format == "csc":
                flag = 1  # CSC format
            else:
                flag = 0  # CSR format

            indices = A.indices.astype(np.intc, copy=False)
            indptr = A.indptr.astype(np.intc, copy=False)
            options = dict(ColPerm=permc_spec)
            x, info = _superlu.gssv(N, A.nnz, A.data, indices, indptr,
                                    b, flag, options=options)
            if info == 0:
                pass  # Success
            elif 0 < info <= N:
                warn("Matrix is exactly singular", MatrixRankWarning, stacklevel=2)
                x.fill(np.nan)
            elif info > N:
                raise MemoryError("Out of memory during gssv")
            else:
                # gssv is not supposed to return any info < 0
                # However, it calls gstrf, which can set info < 0
                raise Exception(f"gssv exited with unknown exit code {info}")
            if b_is_vector:
                x = x.ravel()
        else:
            # b is sparse
            Afactsolve = factorized(A)

            if not (b.format == "csc" or is_pydata_spmatrix(b)):
                warn('spsolve is more efficient when sparse b '
                     'is in the CSC matrix format',
                     SparseEfficiencyWarning, stacklevel=2)
                b = csc_array(b)

            # Create a sparse output matrix by repeatedly applying
            # the sparse factorization to solve columns of b.
            data_segs = []
            row_segs = []
            col_segs = []
            for j in range(b.shape[1]):
                bj = b[:, j].toarray().ravel()
                xj = Afactsolve(bj)
                w = np.flatnonzero(xj)
                segment_length = w.shape[0]
                row_segs.append(w)
                col_segs.append(np.full(segment_length, j, dtype=int))
                data_segs.append(np.asarray(xj[w], dtype=A.dtype))
            sparse_data = np.concatenate(data_segs)
            idx_dtype = get_index_dtype(maxval=max(b.shape))
            sparse_row = np.concatenate(row_segs, dtype=idx_dtype)
            sparse_col = np.concatenate(col_segs, dtype=idx_dtype)
            x = A.__class__((sparse_data, (sparse_row, sparse_col)),
                           shape=b.shape, dtype=A.dtype)

            if is_pydata_sparse:
                x = pydata_sparse_cls.from_scipy_sparse(x)

    return x


def spsolve(data, indices, indptr, b, tol=1e-6, reorder=1):
  """A sparse direct solver using QR factorization.

  Accepts a sparse matrix in CSR format `data, indices, indptr` arrays.
  Currently only the CUDA GPU backend is implemented, the CPU backend will fall
  back to `scipy.sparse.linalg.spsolve`. Neither the CPU nor the GPU
  implementation support batching with `vmap`.

  Args:
    data : An array containing the non-zero entries of the CSR matrix.
    indices : The column indices of the CSR matrix.
    indptr : The row pointer array of the CSR matrix.
    b : The right hand side of the linear system.
    tol : Tolerance to decide if singular or not. Defaults to 1e-6.
    reorder : The reordering scheme to use to reduce fill-in. No reordering if
      ``reorder=0``. Otherwise, symrcm, symamd, or csrmetisnd (``reorder=1,2,3``),
      respectively. Defaults to symrcm.

  Returns:
    An array with the same dtype and size as b representing the solution to
    the sparse linear system.
  """
  return spsolve_p.bind(data, indices, indptr, b, tol=tol, reorder=reorder)

