
def eigh(a: ArrayLike, UPLO="L"):
    a = _atleast_float_1(a)
    return torch.linalg.eigh(a, UPLO=UPLO)


def eigh(a, b=None, *, lower=True, eigvals_only=False, overwrite_a=False,
         overwrite_b=False, type=1, check_finite=True, subset_by_index=None,
         subset_by_value=None, driver=None):
    """
    Solve a standard or generalized eigenvalue problem for a complex
    Hermitian or real symmetric matrix.

    Find eigenvalues array ``w`` and optionally eigenvectors array ``v`` of
    array ``a``, where ``b`` is positive definite such that for every
    eigenvalue λ (i-th entry of w) and its eigenvector ``vi`` (i-th column of
    ``v``) satisfies::

                      a @ vi = λ * b @ vi
        vi.conj().T @ a @ vi = λ
        vi.conj().T @ b @ vi = 1

    In the standard problem, ``b`` is assumed to be the identity matrix.

    Parameters
    ----------
    a : (M, M) array_like
        A complex Hermitian or real symmetric matrix whose eigenvalues and
        eigenvectors will be computed.
    b : (M, M) array_like, optional
        A complex Hermitian or real symmetric definite positive matrix in.
        If omitted, identity matrix is assumed.
    lower : bool, optional
        Whether the pertinent array data is taken from the lower or upper
        triangle of ``a`` and, if applicable, ``b``. (Default: lower)
    eigvals_only : bool, optional
        Whether to calculate only eigenvalues and no eigenvectors.
        (Default: both are calculated)
    overwrite_a : bool, optional
        Whether to overwrite data in ``a`` (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    overwrite_b : bool, optional
        Whether to overwrite data in ``b`` (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    type : int, optional
        For the generalized problems, this keyword specifies the problem type
        to be solved for ``w`` and ``v`` (only takes 1, 2, 3 as possible
        inputs)::

            1 =>     a @ v = w @ b @ v
            2 => a @ b @ v = w @ v
            3 => b @ a @ v = w @ v

        This keyword is ignored for standard problems.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    subset_by_index : iterable, optional
        If provided, this two-element iterable defines the start and the end
        indices of the desired eigenvalues (ascending order and 0-indexed).
        To return only the second smallest to fifth smallest eigenvalues,
        ``[1, 4]`` is used. ``[n-3, n-1]`` returns the largest three. Only
        available with "evr", "evx", and "gvx" drivers. The entries are
        directly converted to integers via ``int()``.
    subset_by_value : iterable, optional
        If provided, this two-element iterable defines the half-open interval
        ``(a, b]`` that, if any, only the eigenvalues between these values
        are returned. Only available with "evr", "evx", and "gvx" drivers. Use
        ``np.inf`` for the unconstrained ends.
    driver : str, optional
        Defines which LAPACK driver should be used. Valid options are "ev",
        "evd", "evr", "evx" for standard problems and "gv", "gvd", "gvx" for
        generalized (where b is not None) problems. See the Notes section.
        The default for standard problems is "evr". For generalized problems,
        "gvd" is used for full set, and "gvx" for subset requested cases.

    Returns
    -------
    w : (N,) ndarray
        The N (N<=M) selected eigenvalues, in ascending order, each
        repeated according to its multiplicity.
    v : (M, N) ndarray
        The normalized eigenvector corresponding to the eigenvalue ``w[i]`` is
        the column ``v[:,i]``. Only returned if ``eigvals_only=False``.

    Raises
    ------
    LinAlgError
        If eigenvalue computation does not converge, an error occurred, or
        b matrix is not definite positive. Note that if input matrices are
        not symmetric or Hermitian, no error will be reported but results will
        be wrong.

    See Also
    --------
    eigvalsh : eigenvalues of symmetric or Hermitian arrays
    eig : eigenvalues and right eigenvectors for non-symmetric arrays
    eigh_tridiagonal : eigenvalues and right eigenvectors for
        symmetric/Hermitian tridiagonal matrices

    Notes
    -----
    This function does not check the input array for being Hermitian/symmetric
    in order to allow for representing arrays with only their upper/lower
    triangular parts. Also, note that even though not taken into account,
    finiteness check applies to the whole array and unaffected by "lower"
    keyword.

    This function uses LAPACK drivers for computations in all possible keyword
    combinations, prefixed with ``sy`` if arrays are real and ``he`` if
    complex, e.g., a float array with "evr" driver is solved via
    "syevr", complex arrays with "gvx" driver problem is solved via "hegvx"
    etc.

    As a brief summary, the slowest and the most robust driver is the
    classical ``<sy/he>ev`` which uses symmetric QR. ``<sy/he>evr`` is seen as
    the optimal choice for the most general cases. However, there are certain
    occasions that ``<sy/he>evd`` computes faster at the expense of more
    memory usage. ``<sy/he>evx``, while still being faster than ``<sy/he>ev``,
    often performs worse than the rest except when very few eigenvalues are
    requested for large arrays though there is still no performance guarantee.

    Note that the underlying LAPACK algorithms are different depending on whether
    `eigvals_only` is True or False --- thus the eigenvalues may differ
    depending on whether eigenvectors are requested or not. The difference is
    generally of the order of machine epsilon times the largest eigenvalue,
    so is likely only visible for zero or nearly zero eigenvalues.

    For the generalized problem, normalization with respect to the given
    type argument::

            type 1 and 3 :      v.conj().T @ a @ v = w
            type 2       : inv(v).conj().T @ a @ inv(v) = w

            type 1 or 2  :      v.conj().T @ b @ v  = I
            type 3       : v.conj().T @ inv(b) @ v  = I


    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import eigh
    >>> A = np.array([[6, 3, 1, 5], [3, 0, 5, 1], [1, 5, 6, 2], [5, 1, 2, 2]])
    >>> w, v = eigh(A)
    >>> np.allclose(A @ v - v @ np.diag(w), np.zeros((4, 4)))
    True

    Request only the eigenvalues

    >>> w = eigh(A, eigvals_only=True)

    Request eigenvalues that are less than 10.

    >>> A = np.array([[34, -4, -10, -7, 2],
    ...               [-4, 7, 2, 12, 0],
    ...               [-10, 2, 44, 2, -19],
    ...               [-7, 12, 2, 79, -34],
    ...               [2, 0, -19, -34, 29]])
    >>> eigh(A, eigvals_only=True, subset_by_value=[-np.inf, 10])
    array([6.69199443e-07, 9.11938152e+00])

    Request the second smallest eigenvalue and its eigenvector

    >>> w, v = eigh(A, subset_by_index=[1, 1])
    >>> w
    array([9.11938152])
    >>> v.shape  # only a single column is returned
    (5, 1)

    """
    # set lower
    uplo = 'L' if lower else 'U'
    # Set job for Fortran routines
    _job = 'N' if eigvals_only else 'V'

    drv_str = [None, "ev", "evd", "evr", "evx", "gv", "gvd", "gvx"]
    if driver not in drv_str:
        raise ValueError('"{}" is unknown. Possible values are "None", "{}".'
                         ''.format(driver, '", "'.join(drv_str[1:])))

    a1 = _asarray_validated(a, check_finite=check_finite)
    if len(a1.shape) != 2 or a1.shape[0] != a1.shape[1]:
        raise ValueError('expected square "a" matrix')

    # accommodate square empty matrices
    if a1.size == 0:
        w_n, v_n = eigh(np.eye(2, dtype=a1.dtype))

        w = np.empty_like(a1, shape=(0,), dtype=w_n.dtype)
        v = np.empty_like(a1, shape=(0, 0), dtype=v_n.dtype)
        if eigvals_only:
            return w
        else:
            return w, v

    overwrite_a = overwrite_a or (_datacopied(a1, a))
    cplx = True if iscomplexobj(a1) else False
    n = a1.shape[0]
    drv_args = {'overwrite_a': overwrite_a}

    if b is not None:
        b1 = _asarray_validated(b, check_finite=check_finite)
        overwrite_b = overwrite_b or _datacopied(b1, b)
        if len(b1.shape) != 2 or b1.shape[0] != b1.shape[1]:
            raise ValueError('expected square "b" matrix')

        if b1.shape != a1.shape:
            raise ValueError(f"wrong b dimensions {b1.shape}, should be {a1.shape}")

        if type not in [1, 2, 3]:
            raise ValueError('"type" keyword only accepts 1, 2, and 3.')

        cplx = True if iscomplexobj(b1) else (cplx or False)
        drv_args.update({'overwrite_b': overwrite_b, 'itype': type})

    subset = (subset_by_index is not None) or (subset_by_value is not None)

    # Both subsets can't be given
    if subset_by_index and subset_by_value:
        raise ValueError('Either index or value subset can be requested.')

    # Check indices if given
    if subset_by_index:
        lo, hi = (int(x) for x in subset_by_index)
        if not (0 <= lo <= hi < n):
            raise ValueError('Requested eigenvalue indices are not valid. '
                             f'Valid range is [0, {n-1}] and start <= end, but '
                             f'start={lo}, end={hi} is given')
        # fortran is 1-indexed
        drv_args.update({'range': 'I', 'il': lo + 1, 'iu': hi + 1})

    if subset_by_value:
        lo, hi = subset_by_value
        if not (-inf <= lo < hi <= inf):
            raise ValueError('Requested eigenvalue bounds are not valid. '
                             'Valid range is (-inf, inf) and low < high, but '
                             f'low={lo}, high={hi} is given')

        drv_args.update({'range': 'V', 'vl': lo, 'vu': hi})

    # fix prefix for lapack routines
    pfx = 'he' if cplx else 'sy'

    # decide on the driver if not given
    # first early exit on incompatible choice
    if driver:
        if b is None and (driver in ["gv", "gvd", "gvx"]):
            raise ValueError(f'{driver} requires input b array to be supplied '
                             'for generalized eigenvalue problems.')
        if (b is not None) and (driver in ['ev', 'evd', 'evr', 'evx']):
            raise ValueError(f'"{driver}" does not accept input b array '
                             'for standard eigenvalue problems.')
        if subset and (driver in ["ev", "evd", "gv", "gvd"]):
            raise ValueError(f'"{driver}" cannot compute subsets of eigenvalues')

    # Default driver is evr and gvd
    else:
        driver = "evr" if b is None else ("gvx" if subset else "gvd")

    lwork_spec = {
                  'syevd': ['lwork', 'liwork'],
                  'syevr': ['lwork', 'liwork'],
                  'heevd': ['lwork', 'liwork', 'lrwork'],
                  'heevr': ['lwork', 'lrwork', 'liwork'],
                  }

    if b is None:  # Standard problem
        drv, drvlw = get_lapack_funcs((pfx + driver, pfx+driver+'_lwork'),
                                      [a1])
        clw_args = {'n': n, 'lower': lower}
        if driver == 'evd':
            clw_args.update({'compute_v': 0 if _job == "N" else 1})

        lw = _compute_lwork(drvlw, **clw_args)
        # Multiple lwork vars
        if isinstance(lw, tuple):
            lwork_args = dict(zip(lwork_spec[pfx+driver], lw))
        else:
            lwork_args = {'lwork': lw}

        drv_args.update({'lower': lower, 'compute_v': 0 if _job == "N" else 1})
        w, v, *other_args, info = drv(a=a1, **drv_args, **lwork_args)

    else:  # Generalized problem
        # 'gvd' doesn't have lwork query
        if driver == "gvd":
            drv = get_lapack_funcs(pfx + "gvd", [a1, b1])
            lwork_args = {}
        else:
            drv, drvlw = get_lapack_funcs((pfx + driver, pfx+driver+'_lwork'),
                                          [a1, b1])
            # generalized drivers use uplo instead of lower
            lw = _compute_lwork(drvlw, n, uplo=uplo)
            lwork_args = {'lwork': lw}

        drv_args.update({'uplo': uplo, 'jobz': _job})

        w, v, *other_args, info = drv(a=a1, b=b1, **drv_args, **lwork_args)

    # m is always the first extra argument
    w = w[:other_args[0]] if subset else w
    v = v[:, :other_args[0]] if (subset and not eigvals_only) else v

    # Check if we had a  successful exit
    if info == 0:
        if eigvals_only:
            return w
        else:
            return w, v
    else:
        if info < -1:
            raise LinAlgError(f'Illegal value in argument {-info} of internal '
                              f'{drv.typecode + pfx + driver}')
        elif info > n:
            raise LinAlgError(f'The leading minor of order {info-n} of B is not '
                              'positive definite. The factorization of B '
                              'could not be completed and no eigenvalues '
                              'or eigenvectors were computed.')
        else:
            drv_err = {'ev': 'The algorithm failed to converge; {} '
                             'off-diagonal elements of an intermediate '
                             'tridiagonal form did not converge to zero.',
                       'evx': '{} eigenvectors failed to converge.',
                       'evd': 'The algorithm failed to compute an eigenvalue '
                              'while working on the submatrix lying in rows '
                              'and columns {0}/{1} through mod({0},{1}).',
                       'evr': 'Internal Error.'
                       }
            if driver in ['ev', 'gv']:
                msg = drv_err['ev'].format(info)
            elif driver in ['evx', 'gvx']:
                msg = drv_err['evx'].format(info)
            elif driver in ['evd', 'gvd']:
                if eigvals_only:
                    msg = drv_err['ev'].format(info)
                else:
                    msg = drv_err['evd'].format(info, n+1)
            else:
                msg = drv_err['evr']

            raise LinAlgError(msg)


def eigh(x: Array, /, xp: Namespace, **kwargs: object) -> EighResult:
    return EighResult(*xp.linalg.eigh(x, **kwargs))


def eigh(a, UPLO='L'):
    """
    Return the eigenvalues and eigenvectors of a complex Hermitian
    (conjugate symmetric) or a real symmetric matrix.

    Returns two objects, a 1-D array containing the eigenvalues of `a`, and
    a 2-D square array or matrix (depending on the input type) of the
    corresponding eigenvectors (in columns).

    Parameters
    ----------
    a : (..., M, M) array
        Hermitian or real symmetric matrices whose eigenvalues and
        eigenvectors are to be computed.
    UPLO : {'L', 'U'}, optional
        Specifies whether the calculation is done with the lower triangular
        part of `a` ('L', default) or the upper triangular part ('U').
        Irrespective of this value only the real parts of the diagonal will
        be considered in the computation to preserve the notion of a Hermitian
        matrix. It therefore follows that the imaginary part of the diagonal
        will always be treated as zero.

    Returns
    -------
    A namedtuple with the following attributes:

    eigenvalues : (..., M) ndarray
        The eigenvalues in ascending order, each repeated according to
        its multiplicity.
    eigenvectors : {(..., M, M) ndarray, (..., M, M) matrix}
        The column ``eigenvectors[:, i]`` is the normalized eigenvector
        corresponding to the eigenvalue ``eigenvalues[i]``.  Will return a
        matrix object if `a` is a matrix object.

    Raises
    ------
    LinAlgError
        If the eigenvalue computation does not converge.

    See Also
    --------
    eigvalsh : eigenvalues of real symmetric or complex Hermitian
               (conjugate symmetric) arrays.
    eig : eigenvalues and right eigenvectors for non-symmetric arrays.
    eigvals : eigenvalues of non-symmetric arrays.
    scipy.linalg.eigh : Similar function in SciPy (but also solves the
                        generalized eigenvalue problem).

    Notes
    -----
    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    The eigenvalues/eigenvectors are computed using LAPACK routines ``_syevd``,
    ``_heevd``.

    The eigenvalues of real symmetric or complex Hermitian matrices are always
    real. [1]_ The array `eigenvalues` of (column) eigenvectors is unitary and
    `a`, `eigenvalues`, and `eigenvectors` satisfy the equations ``dot(a,
    eigenvectors[:, i]) = eigenvalues[i] * eigenvectors[:, i]``.

    References
    ----------
    .. [1] G. Strang, *Linear Algebra and Its Applications*, 2nd Ed., Orlando,
           FL, Academic Press, Inc., 1980, pg. 222.

    Examples
    --------
    >>> import numpy as np
    >>> from numpy import linalg as LA
    >>> a = np.array([[1, -2j], [2j, 5]])
    >>> a
    array([[ 1.+0.j, -0.-2.j],
           [ 0.+2.j,  5.+0.j]])
    >>> eigenvalues, eigenvectors = LA.eigh(a)
    >>> eigenvalues
    array([0.17157288, 5.82842712])
    >>> eigenvectors
    array([[-0.92387953+0.j        , -0.38268343+0.j        ], # may vary
           [ 0.        +0.38268343j,  0.        -0.92387953j]])

    >>> (np.dot(a, eigenvectors[:, 0]) -
    ... eigenvalues[0] * eigenvectors[:, 0])  # verify 1st eigenval/vec pair
    array([5.55111512e-17+0.0000000e+00j, 0.00000000e+00+1.2490009e-16j])
    >>> (np.dot(a, eigenvectors[:, 1]) -
    ... eigenvalues[1] * eigenvectors[:, 1])  # verify 2nd eigenval/vec pair
    array([0.+0.j, 0.+0.j])

    >>> A = np.matrix(a) # what happens if input is a matrix object
    >>> A
    matrix([[ 1.+0.j, -0.-2.j],
            [ 0.+2.j,  5.+0.j]])
    >>> eigenvalues, eigenvectors = LA.eigh(A)
    >>> eigenvalues
    array([0.17157288, 5.82842712])
    >>> eigenvectors
    matrix([[-0.92387953+0.j        , -0.38268343+0.j        ], # may vary
            [ 0.        +0.38268343j,  0.        -0.92387953j]])

    >>> # demonstrate the treatment of the imaginary part of the diagonal
    >>> a = np.array([[5+2j, 9-2j], [0+2j, 2-1j]])
    >>> a
    array([[5.+2.j, 9.-2.j],
           [0.+2.j, 2.-1.j]])
    >>> # with UPLO='L' this is numerically equivalent to using LA.eig() with:
    >>> b = np.array([[5.+0.j, 0.-2.j], [0.+2.j, 2.-0.j]])
    >>> b
    array([[5.+0.j, 0.-2.j],
           [0.+2.j, 2.+0.j]])
    >>> wa, va = LA.eigh(a)
    >>> wb, vb = LA.eig(b)
    >>> wa
    array([1., 6.])
    >>> wb
    array([6.+0.j, 1.+0.j])
    >>> va
    array([[-0.4472136 +0.j        , -0.89442719+0.j        ], # may vary
           [ 0.        +0.89442719j,  0.        -0.4472136j ]])
    >>> vb
    array([[ 0.89442719+0.j       , -0.        +0.4472136j],
           [-0.        +0.4472136j,  0.89442719+0.j       ]])

    """
    UPLO = UPLO.upper()
    if UPLO not in ('L', 'U'):
        raise ValueError("UPLO argument must be 'L' or 'U'")

    a, wrap = _makearray(a)
    _assert_stacked_square(a)
    t, result_t = _commonType(a)

    if UPLO == 'L':
        gufunc = _umath_linalg.eigh_lo
    else:
        gufunc = _umath_linalg.eigh_up

    signature = 'D->dD' if isComplexType(t) else 'd->dd'
    with errstate(call=_raise_linalgerror_eigenvalues_nonconvergence,
                  invalid='call', over='ignore', divide='ignore',
                  under='ignore'):
        w, vt = gufunc(a, signature=signature)
    w = w.astype(_realType(result_t), copy=False)
    vt = vt.astype(result_t, copy=False)
    return EighResult(w, wrap(vt))


def eigh(ctx, A, eigvals_only = False, overwrite_a = False):
    """
    "eigh" is a unified interface for "eigsy" and "eighe". Depending on
    whether A is real or complex the appropriate function is called.

    This routine solves the (ordinary) eigenvalue problem for a real symmetric
    or complex hermitian square matrix A. Given A, an orthogonal (A real) or
    unitary (A complex) matrix Q is calculated which diagonalizes A:

        Q' A Q = diag(E)               and                Q Q' = Q' Q = 1

    Here diag(E) a is diagonal matrix whose diagonal is E.
    ' denotes the hermitian transpose (i.e. ordinary transposition and
    complex conjugation).

    The columns of Q are the eigenvectors of A and E contains the eigenvalues:

        A Q[:,i] = E[i] Q[:,i]

    input:

      A: a real or complex square matrix of format (n,n) which is symmetric
         (i.e. A[i,j]=A[j,i]) or hermitian (i.e. A[i,j]=conj(A[j,i])).

      eigvals_only: if true, calculates only the eigenvalues E.
                    if false, calculates both eigenvectors and eigenvalues.

      overwrite_a: if true, allows modification of A which may improve
                   performance. if false, A is not modified.

    output:

      E: vector of format (n). contains the eigenvalues of A in ascending order.

      Q: an orthogonal or unitary matrix of format (n,n). contains the
         eigenvectors of A as columns.

    return value:

          E         if eigvals_only is true
         (E, Q)     if eigvals_only is false

    example:
      >>> from mpmath import mp
      >>> A = mp.matrix([[3, 2], [2, 0]])
      >>> E = mp.eigh(A, eigvals_only = True)
      >>> print(E)
      [-1.0]
      [ 4.0]

      >>> A = mp.matrix([[1, 2], [2, 3]])
      >>> E, Q = mp.eigh(A)
      >>> print(mp.chop(A * Q[:,0] - E[0] * Q[:,0]))
      [0.0]
      [0.0]

      >>> A = mp.matrix([[1, 2 + 5j], [2 - 5j, 3]])
      >>> E, Q = mp.eigh(A)
      >>> print(mp.chop(A * Q[:,0] - E[0] * Q[:,0]))
      [0.0]
      [0.0]

    see also: eigsy, eighe, eig
    """

    iscomplex = any(type(x) is ctx.mpc for x in A)

    if iscomplex:
        return ctx.eighe(A, eigvals_only = eigvals_only, overwrite_a = overwrite_a)
    else:
        return ctx.eigsy(A, eigvals_only = eigvals_only, overwrite_a = overwrite_a)


def eigh(
    x: Array,
    *,
    lower: bool = True,
    symmetrize_input: bool = True,
    sort_eigenvalues: bool = True,
    subset_by_index: tuple[int, int] | None = None,
    implementation: EighImplementation | None = None,
) -> tuple[Array, Array]:
  r"""Eigendecomposition of a Hermitian matrix.

  Computes the eigenvectors and eigenvalues of a complex Hermitian or real
  symmetric square matrix.

  Args:
    x: A batch of square complex Hermitian or real symmetric matrices with shape
      ``[..., n, n]``.
    lower: If ``symmetrize_input`` is ``False``, describes which triangle of the
      input matrix to use. If ``symmetrize_input`` is ``False``, only the
      triangle given by ``lower`` is accessed; the other triangle is ignored and
      not accessed.
    symmetrize_input: If ``True``, the matrix is symmetrized before the
      eigendecomposition by computing :math:`\frac{1}{2}(x + x^H)`.
    sort_eigenvalues: If ``True``, the eigenvalues will be sorted in ascending
      order. If ``False`` the eigenvalues are returned in an
      implementation-defined order.
    subset_by_index: Optional 2-tuple [start, end] indicating the range of
      indices of eigenvalues to compute. For example, is ``range_select`` =
      [n-2,n], then ``eigh`` computes the two largest eigenvalues and their
      eigenvectors.
    implementation: Optional implementation selection. ``QR`` uses QR-based
      decomposition (default for CPU/GPU). ``JACOBI`` uses Jacobi iteration
      (GPU/TPU only). ``QDWH`` uses QDWH spectral divide-and-conquer
      (default on TPU, TPU only).

  Returns:
    A tuple ``(v, w)``.

    ``v`` is an array with the same dtype as ``x`` such that ``v[..., :, i]`` is
    the normalized eigenvector corresponding to eigenvalue ``w[..., i]``.

    ``w`` is an array with the same dtype as ``x`` (or its real counterpart if
    complex) with shape ``[..., d]`` containing the eigenvalues of ``x`` in
    ascending order(each repeated according to its multiplicity).
    If ``subset_by_index`` is ``None`` then ``d`` is equal to ``n``. Otherwise
    ``d`` is equal to ``subset_by_index[1] - subset_by_index[0]``.
  """
  if symmetrize_input:
    x = symmetrize(x)
  v, w = eigh_p.bind(
      x,
      lower=lower,
      sort_eigenvalues=sort_eigenvalues,
      subset_by_index=subset_by_index,
      algorithm=implementation,
  )
  return v, w


def eigh(a: ArrayLike, UPLO: str | None = None,
         symmetrize_input: bool = True) -> EighResult:
  """
  Compute the eigenvalues and eigenvectors of a Hermitian matrix.

  JAX implementation of :func:`numpy.linalg.eigh`.

  Args:
    a: array of shape ``(..., M, M)``, containing the Hermitian (if complex)
      or symmetric (if real) matrix.
    UPLO: specifies whether the calculation is done with the lower triangular
      part of ``a`` (``'L'``, default) or the upper triangular part (``'U'``).
    symmetrize_input: if True (default) then input is symmetrized, which leads
      to better behavior under automatic differentiation. Note that when this
      is set to True, both the upper and lower triangles of the input will
      be used in computing the decomposition.

  Returns:
    A namedtuple ``(eigenvalues, eigenvectors)`` where

    - ``eigenvalues``: an array of shape ``(..., M)`` containing the eigenvalues,
      sorted in ascending order.
    - ``eigenvectors``: an array of shape ``(..., M, M)``, where column ``v[:, i]`` is the
      normalized eigenvector corresponding to the eigenvalue ``w[i]``.

  See also:
    - :func:`jax.numpy.linalg.eig`: general eigenvalue decomposition.
    - :func:`jax.numpy.linalg.eigvalsh`: compute eigenvalues only.
    - :func:`jax.scipy.linalg.eigh`: SciPy API for Hermitian eigendecomposition.
    - :func:`jax.lax.linalg.eigh`: XLA API for Hermitian eigendecomposition.

  Examples:
    >>> a = jnp.array([[1, -2j],
    ...                [2j, 1]])
    >>> w, v = jnp.linalg.eigh(a)
    >>> w
    Array([-1.,  3.], dtype=float32)
    >>> with jnp.printoptions(precision=3):
    ...   v
    Array([[-0.707+0.j   , -0.707+0.j   ],
           [ 0.   +0.707j,  0.   -0.707j]], dtype=complex64)
  """
  a = ensure_arraylike("jnp.linalg.eigh", a)
  if UPLO is None or UPLO == "L":
    lower = True
  elif UPLO == "U":
    lower = False
  else:
    msg = f"UPLO must be one of None, 'L', or 'U', got {UPLO}"
    raise ValueError(msg)

  a, = promote_dtypes_inexact(a)
  v, w = lax_linalg.eigh(a, lower=lower, symmetrize_input=symmetrize_input)
  return EighResult(w, v)


def eigh(a: ArrayLike, b: ArrayLike | None = None, lower: bool = True,
         eigvals_only: Literal[False] = False, overwrite_a: bool = False,
         overwrite_b: bool = False, turbo: bool = True, eigvals: None = None,
         type: int = 1, check_finite: bool = True) -> tuple[Array, Array]: ...


def eigh(a: ArrayLike, b: ArrayLike | None = None, lower: bool = True, *,
         eigvals_only: Literal[True], overwrite_a: bool = False,
         overwrite_b: bool = False, turbo: bool = True, eigvals: None = None,
         type: int = 1, check_finite: bool = True) -> Array: ...


def eigh(a: ArrayLike, b: ArrayLike | None, lower: bool,
         eigvals_only: Literal[True], overwrite_a: bool = False,
         overwrite_b: bool = False, turbo: bool = True, eigvals: None = None,
         type: int = 1, check_finite: bool = True) -> Array: ...


def eigh(a: ArrayLike, b: ArrayLike | None = None, lower: bool = True,
         eigvals_only: bool = False, overwrite_a: bool = False,
         overwrite_b: bool = False, turbo: bool = True, eigvals: None = None,
         type: int = 1, check_finite: bool = True) -> Array | tuple[Array, Array]: ...


def eigh(a: ArrayLike, b: ArrayLike | None = None, lower: bool = True,
         eigvals_only: bool = False, overwrite_a: bool = False,
         overwrite_b: bool = False, turbo: bool = True, eigvals: None = None,
         type: int = 1, check_finite: bool = True) -> Array | tuple[Array, Array]:
  """Compute eigenvalues and eigenvectors for a Hermitian matrix

  JAX implementation of :func:`scipy.linalg.eigh`.

  Only the standard eigenvalue problem is supported: ``a @ v = lambda * v``.
    The parameter `b` must be None; the generalized problem (``a @ v = lambda * b @ v``)
    is not implemented.

  Args:
    a: Hermitian input array of shape ``(..., N, N)``
    b: Must be None. The generalized eigenvalue problem is not supported.
    lower: if True (default) access only the lower portion of the input matrix.
      Otherwise access only the upper portion.
    eigvals_only: If True, compute only the eigenvalues. If False (default) compute
      both eigenvalues and eigenvectors.
    type: Not used. Only type=1 is supported.

    eigvals: Not used. Only eigvals=None is supported.
    overwrite_a: unused by JAX.
    overwrite_b: unused by JAX.
    turbo: unused by JAX.
    check_finite: unused by JAX.

  Returns:
    A tuple of arrays ``(eigvals, eigvecs)`` if ``eigvals_only`` is False, otherwise
    an array ``eigvals``.

    - ``eigvals``: array of shape ``(..., N)`` containing the eigenvalues.
    - ``eigvecs``: array of shape ``(..., N, N)`` containing the eigenvectors.

  Raise:
    NotImplementedError: If `b` is not None.

  See also:
    - :func:`jax.numpy.linalg.eigh`: NumPy-style eigh API.
    - :func:`jax.lax.linalg.eigh`: XLA-style eigh API.
    - :func:`jax.numpy.linalg.eig`: non-hermitian eigenvalue problem.
    - :func:`jax.scipy.linalg.eigh_tridiagonal`: tri-diagonal eigenvalue problem.

  Examples:
    Compute the standard eigenvalue decomposition of a simple 2x2 matrix:

    >>> a = jnp.array([[2., 1.],
    ...                [1., 2.]])
    >>> eigvals, eigvecs = jax.scipy.linalg.eigh(a)
    >>> eigvals
    Array([1., 3.], dtype=float32)
    >>> eigvecs
    Array([[-0.70710677,  0.70710677],
           [ 0.70710677,  0.70710677]], dtype=float32)

    Eigenvectors are orthonormal:

    >>> jnp.allclose(eigvecs.T @ eigvecs, jnp.eye(2), atol=1E-5)
    Array(True, dtype=bool)

    Solution satisfies the eigenvalue problem:

    >>> jnp.allclose(a @ eigvecs, eigvecs @ jnp.diag(eigvals))
    Array(True, dtype=bool)
  """
  del overwrite_a, overwrite_b, turbo, check_finite  # unused
  return _eigh(a, b, lower, eigvals_only, eigvals, type)


def eigh(
    H,
    *,
    precision='float32',
    termination_size=256,
    n=None,
    sort_eigenvalues=True,
    subset_by_index=None,
):
  """Computes the eigendecomposition of the symmetric/Hermitian matrix H.

  Args:
    H: The `n x n` Hermitian input, padded to `N x N`.
    precision: :class:`~jax.lax.Precision` object specifying the matmul
      precision.
    termination_size: Recursion ends once the blocks reach this linear size.
    n: the true (dynamic) size of the matrix.
    sort_eigenvalues: If `True`, the eigenvalues will be sorted from lowest to
      highest.
    subset_by_index: Optional 2-tuple [start, end] indicating the range of
      indices of eigenvalues to compute. For example, is ``range_select`` =
      [n-2,n], then ``eigh`` computes the two largest eigenvalues and their
      eigenvectors.

  Returns:
    vals: The `n` eigenvalues of `H`.
    vecs: A unitary matrix such that `vecs[:, i]` is a normalized eigenvector
      of `H` corresponding to `vals[i]`. We have `H @ vecs = vals * vecs` up
      to numerical error.
  """
  M, N = H.shape
  if M != N:
    raise TypeError(f"Input H of shape {H.shape} must be square.")
  if n is not None and n > N:
    raise ValueError('Static size must be greater or equal to dynamic size.')

  compute_slice = False
  if subset_by_index is not None:
    compute_slice = subset_by_index != (0, n)
    if len(subset_by_index) != 2:
      raise ValueError('subset_by_index must be a tuple of size 2.')
    if subset_by_index[0] >= subset_by_index[1]:
      raise ValueError('Got empty index range in subset_by_index.')
    if subset_by_index[0] < 0:
      raise ValueError('Indices in subset_by_index must be non-negative.')
    range_max = N if n is None else n
    if subset_by_index[1] > range_max:
      raise ValueError('Index in subset_by_index[1] exceeds matrix size.')

  if N <= termination_size:
    if n is not None:
      H = _mask(H, (n, n))
    eig_vecs, eig_vals = lax_linalg.eigh(
        H, lower=True, sort_eigenvalues=(sort_eigenvalues or compute_slice),
        subset_by_index=None, symmetrize_input=False,
        implementation=lax_linalg.EighImplementation.JACOBI,
    )
    if subset_by_index is not None and compute_slice:
      eig_vals = eig_vals[subset_by_index[0] : subset_by_index[1]]
      eig_vecs = eig_vecs[:, subset_by_index[0] : subset_by_index[1]]
    return eig_vals, eig_vecs

  n = N if n is None else n
  with config.default_matmul_precision(precision):
    eig_vals, eig_vecs = _eigh_work(
        H, n, termination_size=termination_size, subset_by_index=subset_by_index
    )
  eig_vals = _mask(ufuncs.real(eig_vals), (n,), np.nan)
  if sort_eigenvalues or compute_slice:
    sort_idxs = jnp.argsort(eig_vals)
    if compute_slice:
      sort_idxs = sort_idxs[subset_by_index[0] : subset_by_index[1]]
    eig_vals = eig_vals[sort_idxs]
    eig_vecs = eig_vecs[:, sort_idxs]

  return eig_vals, eig_vecs

