
def eig(
    self: Tensor,
    eigenvectors: bool = False,
    *,
    e=None,
    v=None,
) -> tuple[Tensor, Tensor]:
    raise RuntimeError(
        "This function was deprecated since version 1.9 and is now removed. "
        "`torch.linalg.eig` returns complex tensors of dtype `cfloat` or `cdouble` rather than real tensors "
        "mimicking complex tensors.\n\n"
        "L, _ = torch.eig(A) "
        "should be replaced with:\n"
        "L_complex = torch.linalg.eigvals(A)\n\n"
        "and\n\n"
        "L, V = torch.eig(A, eigenvectors=True) "
        "should be replaced with:\n"
        "L_complex, V_complex = torch.linalg.eig(A)"
    )


def eig(a: ArrayLike):
    a = _atleast_float_1(a)
    w, vt = torch.linalg.eig(a)

    if not a.is_complex() and w.is_complex() and (w.imag == 0).all():
        w = w.real
        vt = vt.real
    return w, vt


def eig(expr):
    return EigenValues(expr), EigenVectors(expr)


def eig(a, b=None, left=False, right=True, overwrite_a=False,
        overwrite_b=False, check_finite=True, homogeneous_eigvals=False):
    r"""
    Solve an ordinary or generalized eigenvalue problem of a square matrix.

    Find eigenvalues w and right or left eigenvectors of a general matrix::

        a   @ vr[:, i] = w[i]        * b   @ vr[:, i]
        a.H @ vl[:, i] = w[i].conj() * b.H @ vl[:, i]

    where ``.H`` is the Hermitian conjugation.

    Parameters
    ----------
    a : (..., M, M) array_like
        A complex or real matrix whose eigenvalues and eigenvectors
        will be computed.
    b : (..., M, M) array_like, optional
        Right-hand side matrix in a generalized eigenvalue problem.
        Default is None, identity matrix is assumed.
    left : bool, optional
        Whether to calculate and return left eigenvectors.  Default is False.
    right : bool, optional
        Whether to calculate and return right eigenvectors.  Default is True.
    overwrite_a : bool, optional
        Whether to overwrite `a`; may improve performance.  Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    overwrite_b : bool, optional
        Whether to overwrite `b`; may improve performance.  Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    homogeneous_eigvals : bool, optional
        If True, return the eigenvalues in homogeneous coordinates.
        In this case ``w`` is a ``(2, M)`` array so that::

            w[1, i] * a @ vr[:, i] = w[0, i] * b @ vr[:, i]

        This option is sometimes useful for generalized eigenvalue problems,
        ``b is not None``, where an eigenvalue, :math:`\lambda = \alpha / \beta`  ,
        can over- or underflow; typically, :\math:`\alpha` and :math:`\beta` are of the
        order of ``norm(a)`` and ``norm(b)``, respectively.

        Default is False.

    Returns
    -------
    w : (..., M,) or (..., 2, M) complex ndarray
        The eigenvalues, each repeated according to its
        multiplicity. The shape is ``(..., M)`` unless ``homogeneous_eigvals=True``.
    vl : (..., M, M) double or complex ndarray
        The left eigenvector corresponding to the eigenvalue
        ``w[i]`` is the column ``vl[:, i]``. Only returned if ``left=True``.
        The left eigenvector is not normalized.
    vr : (..., M, M) double or complex ndarray
        The normalized right eigenvector corresponding to the eigenvalue
        ``w[i]`` is the column ``vr[:, i]``.  Only returned if ``right=True`` (default).

    Raises
    ------
    LinAlgError
        If eigenvalue computation does not converge.

    See Also
    --------
    eigvals : eigenvalues of general arrays
    eigh : Eigenvalues and right eigenvectors for symmetric/Hermitian arrays.
    eig_banded : eigenvalues and right eigenvectors for symmetric/Hermitian
        band matrices
    eigh_tridiagonal : eigenvalues and right eigenvectors for
        symmetric/Hermitian tridiagonal matrices

    Notes
    -----
    Array arguments of this function, `a` and `b`, may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import linalg
    >>> a = np.array([[0., -1.],
    ...               [1.,  0.]])

    Compute the eigenvalues (``eigvals`` is the same as ``eig(a, right=False)``)

    >>> linalg.eigvals(a)
    array([0.+1.j, 0.-1.j])

    Solve a generalized eigenvalue problem:

    >>> b = np.array([[0., 1.], [1., 1.]])
    >>> linalg.eigvals(a, b)
    array([ 1.+0.j, -1.+0.j])

    Inputs with ``ndim > 2`` are interpreted as a batch of matrices

    >>> a2 = np.stack((a, 2*a))
    >>> linalg.eigvals(a2)
    array([[0.+1.j, 0.-1.j],
           [0.+2.j, 0.-2.j]])

    ``homogeneous_eigvals=True`` argument effectively separates each eigenvalue into a
    numerator-denominator pair:

    >>> a = np.array([[3., 0., 0.],
    ...               [0., 8., 0.],
    ...               [0., 0., 7.]])
    >>> b = 2*np.eye(3)
    >>> linalg.eigvals(a, b, homogeneous_eigvals=True)
    array([[3.+0.j, 8.+0.j, 7.+0.j],
           [2.+0.j, 2.+0.j, 2.+0.j]])

    **Eigenvectors**: by default, ``eig`` returns normalized right eigenvectors in
    columns of the second return array

    >>> a = np.array([[0., -1.],
    ...               [1., 0.]])
    >>> w, vr = linalg.eig(a)
    >>> w      # eigenvalues
    array([0. + 1.j, 0. - 1.j])
    >>> vr     # normalized right eigenvectors
    array([[0.70710678 + 0.j        , 0.70710678 - 0.j        ],
           [0.         - 0.70710678j, 0.         + 0.70710678j]])

    Verify that columns of ``vr`` are indeed eigenvectors:

    >>> a @ vr[:, 0] - w[0] * vr[:, 0]
    array([0.+0.j, 0.+0.j])
    >>> a @ vr[:, 1] - w[1] * vr[:, 1]
    array([0.+0.j, 0.+0.j])

    To compute the normalized left eigenvectors, use ``left=True``:

    >>> w, vl, vr = linalg.eig(a, left=True, right=True)
    >>> vl * np.sqrt(2)   # ``vl`` is normalized left eigenvectors
    array([[-1. + 0.j, -1. - 0.j],
           [ 0. + 1.j,  0. - 1.j]])
    >>> vr * np.sqrt(2)   # ``vr`` is normalized right eigenvectors
    array([[1. + 0.j, 1. + 0.j],
           [0. - 1.j, 0. + 1.j]])
    """
    # basic sanity checks of the input matrix
    a1 = _asarray_validated(a, check_finite=check_finite)
    _deprecate_dtypes("eig", a1)

    if len(a1.shape) < 2 or a1.shape[-1] != a1.shape[-2]:
        raise ValueError(
            f"Expected a square matrix or a batch of square matrices. Got {a.shape = }"
        )

    # Also check if dtype is LAPACK compatible
    a1, overwrite_a = _normalize_lapack_dtype(a1, overwrite_a)
    a1, overwrite_a = _ensure_aligned_and_native(a1, overwrite_a)

    overwrite_a = overwrite_a or (_datacopied(a1, a))
    overwrite_a = overwrite_a and (a1.ndim == 2) and (a1.flags["F_CONTIGUOUS"])

    # accommodate empty arrays
    if a1.shape[-1] == 0 or a1.shape[-2] == 0:
        batch_shape = a1.shape[:-2]
        w_n, vr_n = eig(np.eye(2, dtype=a1.dtype))
        w = np.empty(batch_shape + (0,), dtype=w_n.dtype)
        w = _make_eigvals(w, None, homogeneous_eigvals)
        vl = np.empty(batch_shape + (0, 0), dtype=vr_n.dtype)
        vr = np.empty(batch_shape + (0, 0), dtype=vr_n.dtype)
        if not (left or right):
            return w
        if left:
            if right:
                return w, vl, vr
            return w, vl
        return w, vr

    if b is None:
        # regular eigenvalue problem
        w, beta, vl, vr, err_lst  = _batched_linalg._eig(
            a1, left, right, overwrite_a, False
        )

        if err_lst:
            _check_format_errors_warnings("geev", err_lst)

    else:
        # b is not None: generalized eigenvalue problem

        b1 = _asarray_validated(b, check_finite=check_finite)
        _deprecate_dtypes("eig", b1)

        a1, b1 = _ensure_dtype_cdsz(a1, b1)  # NB: makes a1.dtype == b1.dtype, if needed
        b1, overwrite_b = _ensure_aligned_and_native(b1, overwrite_b)

        if len(b1.shape) < 2 or b1.shape[-1] != b1.shape[-2]:
            raise ValueError('expected square matrix')

        if a1.shape[-1] != b1.shape[-1]:
            raise ValueError('a and b must have the same shape')

        # broadcast batch dimensions of b1 and a1
        batch_shape = np.broadcast_shapes(a1.shape[:-2], b1.shape[:-2])
        a1 = np.broadcast_to(a1, batch_shape + a1.shape[-2:])
        b1 = np.broadcast_to(b1, batch_shape + b1.shape[-2:])

        # check if we can work in-place (a1 might have been broadcast by b1)
        overwrite_a = overwrite_a and (a1.ndim == 2)

        overwrite_b = overwrite_b or (_datacopied(b1, b))
        overwrite_b = overwrite_b and (b1.ndim == 2) and (b1.flags["F_CONTIGUOUS"])

        w, beta, vl, vr, err_lst = _batched_linalg._eig(
            a1, left, right, overwrite_a, overwrite_b, b1
        )

        if err_lst:
            _check_format_errors_warnings("ggev", err_lst)

        # eigenvectors returned by ?GGEV are NOT normalized
        if right:
            vr /= np.linalg.vector_norm(vr, axis=-2, keepdims=True)
        if left:
            vl /= np.linalg.vector_norm(vl, axis=-2, keepdims=True)

    w = _make_eigvals(w, beta, homogeneous_eigvals)

    # backwards compat: make eigvecs real if all eigenvalues have zero imaginary parts
    a_is_real = a1.dtype in (np.float32, np.float64)
    if a_is_real and (w.imag == 0).all():
        if left:
            vl = vl.real
        if right:
            vr = vr.real

    if not (left or right):
        return w
    if left:
        if right:
            return w, vl, vr
        return w, vl
    return w, vr


def eig(x: Array, /) -> tuple[Array, Array]:
    try:
        from numpy.linalg._linalg import (  # type: ignore[attr-defined]
            _assert_stacked_square,
            _assert_finite,
            _commonType,
            _makearray,
            _raise_linalgerror_eigenvalues_nonconvergence,
            isComplexType,
            _complexType,
        )
    except ImportError:
        from numpy.linalg.linalg import (  # type: ignore[attr-defined]
            _assert_stacked_square,
            _assert_finite,
            _commonType,
            _makearray,
            _raise_linalgerror_eigenvalues_nonconvergence,
            isComplexType,
            _complexType,
        )
    from numpy.linalg import _umath_linalg

    x, wrap = _makearray(x)
    _assert_stacked_square(x)
    _assert_finite(x)
    t, result_t = _commonType(x)

    signature = 'D->DD' if isComplexType(t) else 'd->DD'
    with np.errstate(call=_raise_linalgerror_eigenvalues_nonconvergence,
                  invalid='call', over='ignore', divide='ignore',
                  under='ignore'):
        w, vt = _umath_linalg.eig(x, signature=signature)

    result_t = _complexType(result_t)
    vt = vt.astype(result_t, copy=False)
    return EigResult(w.astype(result_t, copy=False), wrap(vt))


def eig(a):
    """
    Compute the eigenvalues and right eigenvectors of a square array.

    Parameters
    ----------
    a : (..., M, M) array
        Matrices for which the eigenvalues and right eigenvectors will
        be computed

    Returns
    -------
    A namedtuple with the following attributes:

    eigenvalues : (..., M) array
        The eigenvalues, each repeated according to its multiplicity.
        The eigenvalues are not necessarily ordered. The resulting
        array will be of complex type, unless the imaginary part is
        zero in which case it will be cast to a real type. When `a`
        is real the resulting eigenvalues will be real (0 imaginary
        part) or occur in conjugate pairs

    eigenvectors : (..., M, M) array
        The normalized (unit "length") eigenvectors, such that the
        column ``eigenvectors[:,i]`` is the eigenvector corresponding to the
        eigenvalue ``eigenvalues[i]``.

    Raises
    ------
    LinAlgError
        If the eigenvalue computation does not converge.

    See Also
    --------
    eigvals : eigenvalues of a non-symmetric array.
    eigh : eigenvalues and eigenvectors of a real symmetric or complex
           Hermitian (conjugate symmetric) array.
    eigvalsh : eigenvalues of a real symmetric or complex Hermitian
               (conjugate symmetric) array.
    scipy.linalg.eig : Similar function in SciPy that also solves the
                       generalized eigenvalue problem.
    scipy.linalg.schur : Best choice for unitary and other non-Hermitian
                         normal matrices.

    Notes
    -----
    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    This is implemented using the ``_geev`` LAPACK routines which compute
    the eigenvalues and eigenvectors of general square arrays.

    The number `w` is an eigenvalue of `a` if there exists a vector `v` such
    that ``a @ v = w * v``. Thus, the arrays `a`, `eigenvalues`, and
    `eigenvectors` satisfy the equations ``a @ eigenvectors[:,i] =
    eigenvalues[i] * eigenvectors[:,i]`` for :math:`i \\in \\{0,...,M-1\\}`.

    The array `eigenvectors` may not be of maximum rank, that is, some of the
    columns may be linearly dependent, although round-off error may obscure
    that fact. If the eigenvalues are all different, then theoretically the
    eigenvectors are linearly independent and `a` can be diagonalized by a
    similarity transformation using `eigenvectors`, i.e, ``inv(eigenvectors) @
    a @ eigenvectors`` is diagonal.

    For non-Hermitian normal matrices the SciPy function `scipy.linalg.schur`
    is preferred because the matrix `eigenvectors` is guaranteed to be
    unitary, which is not the case when using `eig`. The Schur factorization
    produces an upper triangular matrix rather than a diagonal matrix, but for
    normal matrices only the diagonal of the upper triangular matrix is
    needed, the rest is roundoff error.

    Finally, it is emphasized that `eigenvectors` consists of the *right* (as
    in right-hand side) eigenvectors of `a`. A vector `y` satisfying ``y.T @ a
    = z * y.T`` for some number `z` is called a *left* eigenvector of `a`,
    and, in general, the left and right eigenvectors of a matrix are not
    necessarily the (perhaps conjugate) transposes of each other.

    References
    ----------
    G. Strang, *Linear Algebra and Its Applications*, 2nd Ed., Orlando, FL,
    Academic Press, Inc., 1980, Various pp.

    Examples
    --------
    >>> import numpy as np
    >>> from numpy import linalg as LA

    (Almost) trivial example with real eigenvalues and eigenvectors.

    >>> eigenvalues, eigenvectors = LA.eig(np.diag((1, 2, 3)))
    >>> eigenvalues
    array([1. + 0j, 2. + 0j, 3. + 0j])
    >>> eigenvectors.real
    array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]])

    Real matrix possessing complex eigenvalues and eigenvectors;
    note that the eigenvalues are complex conjugates of each other.

    >>> eigenvalues, eigenvectors = LA.eig(np.array([[1, -1], [1, 1]]))
    >>> eigenvalues
    array([1.+1.j, 1.-1.j])
    >>> eigenvectors
    array([[0.70710678+0.j        , 0.70710678-0.j        ],
           [0.        -0.70710678j, 0.        +0.70710678j]])

    Complex-valued matrix with real eigenvalues (but complex-valued
    eigenvectors); note that ``a.conj().T == a``, i.e., `a` is Hermitian.

    >>> a = np.array([[1, 1j], [-1j, 1]])
    >>> eigenvalues, eigenvectors = LA.eig(a)
    >>> eigenvalues
    array([2.+0.j, 0.+0.j])
    >>> eigenvectors
    array([[ 0.        +0.70710678j,  0.70710678+0.j        ], # may vary
           [ 0.70710678+0.j        , -0.        +0.70710678j]])

    Be careful about round-off error!

    >>> a = np.array([[1 + 1e-9, 0], [0, 1 - 1e-9]])
    >>> # Theor. eigenvalues are 1 +/- 1e-9
    >>> eigenvalues, eigenvectors = LA.eig(a)
    >>> eigenvalues
    array([1.+0j, 1.+0j])
    >>> eigenvectors.real
    array([[1., 0.],
           [0., 1.]])

    """
    a, wrap = _makearray(a)
    _assert_stacked_square(a)
    _assert_finite(a)
    t, result_t = _commonType(a)

    signature = 'D->DD' if isComplexType(t) else 'd->DD'
    with errstate(call=_raise_linalgerror_eigenvalues_nonconvergence,
                  invalid='call', over='ignore', divide='ignore',
                  under='ignore'):
        w, vt = _umath_linalg.eig(a, signature=signature)

    w = w.astype(_complexType(result_t), copy=False)
    vt = vt.astype(_complexType(result_t), copy=False)
    return EigResult(w, wrap(vt))


def eig(ctx, A, left = False, right = True, overwrite_a = False):
    """
    This routine computes the eigenvalues and optionally the left and right
    eigenvectors of a square matrix A. Given A, a vector E and matrices ER
    and EL are calculated such that

                        A ER[:,i] =         E[i] ER[:,i]
                EL[i,:] A         = EL[i,:] E[i]

    E contains the eigenvalues of A. The columns of ER contain the right eigenvectors
    of A whereas the rows of EL contain the left eigenvectors.


    input:
      A           : a real or complex square matrix of shape (n, n)
      left        : if true, the left eigenvectors are calculated.
      right       : if true, the right eigenvectors are calculated.
      overwrite_a : if true, allows modification of A which may improve
                    performance. if false, A is not modified.

    output:
      E    : a list of length n containing the eigenvalues of A.
      ER   : a matrix whose columns contain the right eigenvectors of A.
      EL   : a matrix whose rows contain the left eigenvectors of A.

    return values:
       E            if left and right are both false.
      (E, ER)       if right is true and left is false.
      (E, EL)       if left is true and right is false.
      (E, EL, ER)   if left and right are true.


    examples:
      >>> from mpmath import mp
      >>> A = mp.matrix([[3, -1, 2], [2, 5, -5], [-2, -3, 7]])
      >>> E, ER = mp.eig(A)
      >>> print(mp.chop(A * ER[:,0] - E[0] * ER[:,0]))
      [0.0]
      [0.0]
      [0.0]

      >>> E, EL, ER = mp.eig(A,left = True, right = True)
      >>> E, EL, ER = mp.eig_sort(E, EL, ER)
      >>> mp.nprint(E)
      [2.0, 4.0, 9.0]
      >>> print(mp.chop(A * ER[:,0] - E[0] * ER[:,0]))
      [0.0]
      [0.0]
      [0.0]
      >>> print(mp.chop( EL[0,:] * A - EL[0,:] * E[0]))
      [0.0  0.0  0.0]

    warning:
     - If there are multiple eigenvalues, the eigenvectors do not necessarily
       span the whole vectorspace, i.e. ER and EL may have not full rank.
       Furthermore in that case the eigenvectors are numerical ill-conditioned.
     - In the general case the eigenvalues have no natural order.

    see also:
      - eigh (or eigsy, eighe) for the symmetric eigenvalue problem.
      - eig_sort for sorting of eigenvalues and eigenvectors
    """

    n = A.rows

    if n == 1:
        if left and (not right):
            return ([A[0]], ctx.matrix([[1]]))

        if right and (not left):
            return ([A[0]], ctx.matrix([[1]]))

        return ([A[0]], ctx.matrix([[1]]), ctx.matrix([[1]]))

    if not overwrite_a:
        A = A.copy()

    T = ctx.zeros(n, 1)

    hessenberg_reduce_0(ctx, A, T)

    if left or right:
        Q = A.copy()
        hessenberg_reduce_1(ctx, Q, T)
    else:
        Q = False

    for x in xrange(n):
        for y in xrange(x + 2, n):
            A[y,x] = 0

    hessenberg_qr(ctx, A, Q)

    E = [0 for i in xrange(n)]
    for i in xrange(n):
        E[i] = A[i,i]

    if not (left or right):
        return E

    if left:
        EL = eig_tr_l(ctx, A)
        EL = EL * Q.transpose_conj()

    if right:
        ER = eig_tr_r(ctx, A)
        ER = Q * ER

    if left and (not right):
        return (E, EL)

    if right and (not left):
        return (E, ER)

    return (E, EL, ER)


def eig(
    x: ArrayLike,
    *,
    compute_left_eigenvectors: bool = True,
    compute_right_eigenvectors: bool = True,
    enable_eigvec_derivs: bool = False,
    implementation: EigImplementation | None = None,
    use_magma: bool | None = None,
) -> list[Array]:
  """Eigendecomposition of a general matrix.

  Nonsymmetric eigendecomposition is only implemented on CPU and GPU. On GPU,
  the default implementation calls LAPACK directly on the host CPU, but an
  experimental GPU implementation using `MAGMA <https://icl.utk.edu/magma/>`_
  is also available. The MAGMA implementation is typically slower than the
  equivalent LAPACK implementation for small matrices (less than about 2048),
  but it may perform better for larger matrices.

  To enable the MAGMA implementation, you must install MAGMA yourself (there
  are Debian and conda-forge packages, or you can build from source). Then set
  the ``use_magma`` argument to ``True``, or set the ``jax_use_magma``
  configuration variable to ``"on"`` or ``"auto"``:

  .. code-block:: python

      jax.config.update('jax_use_magma', 'on')

  JAX will try to ``dlopen`` the installed MAGMA shared library, raising an
  error if it is not found. To explicitly specify the path to the MAGMA
  library, set the environment variable `JAX_GPU_MAGMA_PATH` to the full
  installation path.

  If ``jax_use_magma`` is set to ``"auto"``, the MAGMA implementation will
  be used if the library can be found, and the input matrix is sufficiently
  large (>= 2048x2048).

  Args:
    x: A batch of square matrices with shape ``[..., n, n]``.
    compute_left_eigenvectors: If true, the left eigenvectors will be computed.
    compute_right_eigenvectors: If true, the right eigenvectors will be
      computed.
    enable_eigvec_derivs: If true, enable autodiff of the returned
      eigenvectors. The eigenvector derivative is taken under the LAPACK
      ``geev`` normalisation (each eigenvector has unit 2-norm and its
      largest-magnitude component is real). It is only valid when (i) all
      eigenvalues are distinct and (ii) no eigenvector has two components
      tied for largest magnitude. Defaults to ``False`` because these
      conditions cannot be checked statically; see
      https://github.com/jax-ml/jax/issues/2748 for discussion.
    use_magma: Deprecated, please use ``implementation`` instead. Locally
      override the ``jax_use_magma`` flag. If ``True``, the eigendecomposition
      is computed using MAGMA. If ``False``, the computation is done using
      LAPACK on to the host CPU. If ``None`` (default), the behavior is
      controlled by the ``jax_use_magma`` flag. This argument is only used on
      GPU. Will be removed in JAX 0.9.
    implementation: Controls the choice of eigendecomposition algorithm. If
    ``LAPACK``, the computation will be performed using LAPACK on the host CPU.
      If ``MAGMA``, the computation will be performed using the MAGMA library on
      the GPU. If ``CUSOLVER``, the computation will be performed using the
      Cusolver library on the GPU. The ``CUSOLVER`` implementation requires
      Cusolver 11.7.1 (from CUDA 12.6 update 2) to be installed, and does not
      support computing left eigenvectors.
      If ``None`` (default), an automatic choice will be made, depending on the
      Cusolver version, whether left eigenvectors were requested, and the
      ``jax_use_magma`` configuration variable.

  Returns:
    The eigendecomposition of ``x``, which is a tuple of the form
    ``(w, vl, vr)`` where ``w`` are the eigenvalues, ``vl`` are the left
    eigenvectors, and ``vr`` are the right eigenvectors. ``vl`` and ``vr`` are
    optional and will only be included if ``compute_left_eigenvectors`` or
    ``compute_right_eigenvectors`` respectively are ``True``.

    If the eigendecomposition fails, then arrays full of NaNs will be returned
    for that batch element.
  """
  if use_magma is not None:
    warnings.warn(
        "use_magma is deprecated, please use"
        " implementation=EigImplementation.MAGMA instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    implementation = (
        EigImplementation.MAGMA if use_magma else EigImplementation.LAPACK
    )
  return eig_p.bind(x, compute_left_eigenvectors=compute_left_eigenvectors,
                    compute_right_eigenvectors=compute_right_eigenvectors,
                    enable_eigvec_derivs=enable_eigvec_derivs,
                    implementation=implementation)


def eig(a: ArrayLike) -> EigResult:
  """
  Compute the eigenvalues and eigenvectors of a square array.

  JAX implementation of :func:`numpy.linalg.eig`.

  Args:
    a: array of shape ``(..., M, M)`` for which to compute the eigenvalues and vectors.

  Returns:
    A namedtuple ``(eigenvalues, eigenvectors)``. The namedtuple has fields:

    - ``eigenvalues``: an array of shape ``(..., M)`` containing the eigenvalues.
    - ``eigenvectors``: an array of shape ``(..., M, M)``, where column ``v[:, i]`` is the
      eigenvector corresponding to the eigenvalue ``w[i]``.

  Notes:
    - This differs from :func:`numpy.linalg.eig` in that the return type of
      :func:`jax.numpy.linalg.eig` is always complex64 for 32-bit input, and complex128
      for 64-bit input.
    - At present, non-symmetric eigendecomposition is only implemented on the CPU and
      GPU backends. For more details about the GPU implementation, see the
      documentation for :func:`jax.lax.linalg.eig`.
    - Currently autodiff is not supported for computation of non-symmetric eigenvectors;
      see https://github.com/jax-ml/jax/issues/2748.

  See also:
    - :func:`jax.lax.linalg.eig`: similar function with different eigenvector options
      and device-specific implementations.
    - :func:`jax.numpy.linalg.eigh`: eigenvectors and eigenvalues of a Hermitian matrix.
    - :func:`jax.numpy.linalg.eigvals`: compute eigenvalues only.

  Examples:
    >>> a = jnp.array([[1., 2.],
    ...                [2., 1.]])
    >>> w, v = jnp.linalg.eig(a)
    >>> with jax.numpy.printoptions(precision=4):
    ...   w
    Array([ 3.+0.j, -1.+0.j], dtype=complex64)
    >>> v
    Array([[ 0.70710677+0.j, -0.70710677+0.j],
           [ 0.70710677+0.j,  0.70710677+0.j]], dtype=complex64)
  """
  a = ensure_arraylike("jnp.linalg.eig", a)
  a, = promote_dtypes_inexact(a)
  w, v = lax_linalg.eig(a, compute_left_eigenvectors=False)
  return EigResult(w, v)

