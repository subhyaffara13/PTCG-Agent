
def eigvalsh(a: ArrayLike, UPLO="L"):
    a = _atleast_float_1(a)
    return torch.linalg.eigvalsh(a, UPLO=UPLO)


def eigvalsh(a, b=None, *, lower=True, overwrite_a=False,
             overwrite_b=False, type=1, check_finite=True, subset_by_index=None,
             subset_by_value=None, driver=None):
    """
    Solves a standard or generalized eigenvalue problem for a complex
    Hermitian or real symmetric matrix.

    Find eigenvalues array ``w`` of array ``a``, where ``b`` is positive
    definite such that for every eigenvalue λ (i-th entry of w) and its
    eigenvector vi (i-th column of v) satisfies::

                      a @ vi = λ * b @ vi
        vi.conj().T @ a @ vi = λ
        vi.conj().T @ b @ vi = 1

    In the standard problem, b is assumed to be the identity matrix.

    Parameters
    ----------
    a : (M, M) array_like
        A complex Hermitian or real symmetric matrix whose eigenvalues will
        be computed.
    b : (M, M) array_like, optional
        A complex Hermitian or real symmetric definite positive matrix in.
        If omitted, identity matrix is assumed.
    lower : bool, optional
        Whether the pertinent array data is taken from the lower or upper
        triangle of ``a`` and, if applicable, ``b``. (Default: lower)
    overwrite_a : bool, optional
        Whether to overwrite data in ``a`` (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    overwrite_b : bool, optional
        Whether to overwrite data in ``b`` (may improve performance). Default
        is False.
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
        generalized (where b is not None) problems. See the Notes section of
        `scipy.linalg.eigh`.

    Returns
    -------
    w : (N,) ndarray
        The N (N<=M) selected eigenvalues, in ascending order, each
        repeated according to its multiplicity.

    Raises
    ------
    LinAlgError
        If eigenvalue computation does not converge, an error occurred, or
        b matrix is not definite positive. Note that if input matrices are
        not symmetric or Hermitian, no error will be reported but results will
        be wrong.

    See Also
    --------
    eigh : eigenvalues and right eigenvectors for symmetric/Hermitian arrays
    eigvals : eigenvalues of general arrays
    eigvals_banded : eigenvalues for symmetric/Hermitian band matrices
    eigvalsh_tridiagonal : eigenvalues of symmetric/Hermitian tridiagonal
        matrices

    Notes
    -----
    This function does not check the input array for being Hermitian/symmetric
    in order to allow for representing arrays with only their upper/lower
    triangular parts.

    This function serves as a one-liner shorthand for `scipy.linalg.eigh` with
    the option ``eigvals_only=True`` to get the eigenvalues and not the
    eigenvectors. Here it is kept as a legacy convenience. It might be
    beneficial to use the main function to have full control and to be a bit
    more pythonic.

    Examples
    --------
    For more examples see `scipy.linalg.eigh`.

    >>> import numpy as np
    >>> from scipy.linalg import eigvalsh
    >>> A = np.array([[6, 3, 1, 5], [3, 0, 5, 1], [1, 5, 6, 2], [5, 1, 2, 2]])
    >>> w = eigvalsh(A)
    >>> w
    array([-3.74637491, -0.76263923,  6.08502336, 12.42399079])

    """
    return eigh(a, b=b, lower=lower, eigvals_only=True, overwrite_a=overwrite_a,
                overwrite_b=overwrite_b, type=type, check_finite=check_finite,
                subset_by_index=subset_by_index, subset_by_value=subset_by_value,
                driver=driver)


def eigvalsh(a, UPLO='L'):
    """
    Compute the eigenvalues of a complex Hermitian or real symmetric matrix.

    Main difference from eigh: the eigenvectors are not computed.

    Parameters
    ----------
    a : (..., M, M) array_like
        A complex- or real-valued matrix whose eigenvalues are to be
        computed.
    UPLO : {'L', 'U'}, optional
        Specifies whether the calculation is done with the lower triangular
        part of `a` ('L', default) or the upper triangular part ('U').
        Irrespective of this value only the real parts of the diagonal will
        be considered in the computation to preserve the notion of a Hermitian
        matrix. It therefore follows that the imaginary part of the diagonal
        will always be treated as zero.

    Returns
    -------
    w : (..., M,) ndarray
        The eigenvalues in ascending order, each repeated according to
        its multiplicity.

    Raises
    ------
    LinAlgError
        If the eigenvalue computation does not converge.

    See Also
    --------
    eigh : eigenvalues and eigenvectors of real symmetric or complex Hermitian
           (conjugate symmetric) arrays.
    eigvals : eigenvalues of general real or complex arrays.
    eig : eigenvalues and right eigenvectors of general real or complex
          arrays.
    scipy.linalg.eigvalsh : Similar function in SciPy.

    Notes
    -----
    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    The eigenvalues are computed using LAPACK routines ``_syevd``, ``_heevd``.

    Examples
    --------
    >>> import numpy as np
    >>> from numpy import linalg as LA
    >>> a = np.array([[1, -2j], [2j, 5]])
    >>> LA.eigvalsh(a)
    array([ 0.17157288,  5.82842712]) # may vary

    >>> # demonstrate the treatment of the imaginary part of the diagonal
    >>> a = np.array([[5+2j, 9-2j], [0+2j, 2-1j]])
    >>> a
    array([[5.+2.j, 9.-2.j],
           [0.+2.j, 2.-1.j]])
    >>> # with UPLO='L' this is numerically equivalent to using LA.eigvals()
    >>> # with:
    >>> b = np.array([[5.+0.j, 0.-2.j], [0.+2.j, 2.-0.j]])
    >>> b
    array([[5.+0.j, 0.-2.j],
           [0.+2.j, 2.+0.j]])
    >>> wa = LA.eigvalsh(a)
    >>> wb = LA.eigvals(b)
    >>> wa
    array([1., 6.])
    >>> wb
    array([6.+0.j, 1.+0.j])

    """
    UPLO = UPLO.upper()
    if UPLO not in ('L', 'U'):
        raise ValueError("UPLO argument must be 'L' or 'U'")

    if UPLO == 'L':
        gufunc = _umath_linalg.eigvalsh_lo
    else:
        gufunc = _umath_linalg.eigvalsh_up

    a, wrap = _makearray(a)
    _assert_stacked_square(a)
    t, result_t = _commonType(a)
    signature = 'D->d' if isComplexType(t) else 'd->d'
    with errstate(call=_raise_linalgerror_eigenvalues_nonconvergence,
                  invalid='call', over='ignore', divide='ignore',
                  under='ignore'):
        w = gufunc(a, signature=signature)
    return w.astype(_realType(result_t), copy=False)


def eigvalsh(a: ArrayLike, UPLO: str | None = 'L', *,
             symmetrize_input: bool = True) -> Array:
  """
  Compute the eigenvalues of a Hermitian matrix.

  JAX implementation of :func:`numpy.linalg.eigvalsh`.

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
    An array of shape ``(..., M)`` containing the eigenvalues, sorted in
    ascending order.

  See also:
    - :func:`jax.numpy.linalg.eig`: general eigenvalue decomposition.
    - :func:`jax.numpy.linalg.eigh`: computes eigenvalues and eigenvectors of a
      Hermitian matrix.

  Examples:
    >>> a = jnp.array([[1, -2j],
    ...                [2j, 1]])
    >>> w = jnp.linalg.eigvalsh(a)
    >>> w
    Array([-1.,  3.], dtype=float32)
  """
  a = ensure_arraylike("jnp.linalg.eigvalsh", a)
  a, = promote_dtypes_inexact(a)
  w, _ = eigh(a, UPLO, symmetrize_input=symmetrize_input)
  return w

