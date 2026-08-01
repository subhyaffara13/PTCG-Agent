
def cholesky(self: Tensor, upper: bool = False) -> Tensor:
    if self.numel() == 0:
        return torch.empty_like(self, memory_format=torch.legacy_contiguous_format)
    squareCheckInputs(self, "cholesky")
    return cloneBatchedColumnMajor(self)


def cholesky(a: ArrayLike):
    a = _atleast_float_1(a)
    return torch.linalg.cholesky(a)


def cholesky(a, lower=False, overwrite_a=False, check_finite=True):
    """
    Compute the Cholesky decomposition of a matrix.

    Returns the Cholesky decomposition, :math:`A = L L^*` or
    :math:`A = U^* U` of a Hermitian positive-definite matrix A.

    Parameters
    ----------
    a : (..., M, M) array_like
        Matrix to be decomposed
    lower : bool, optional
        Whether to compute the upper- or lower-triangular Cholesky
        factorization. During decomposition, only the selected half of the
        matrix is referenced. Default is upper-triangular.
    overwrite_a : bool, optional
        Whether to overwrite data in `a` (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the entire input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    c : (..., M, M) ndarray
        Upper- or lower-triangular Cholesky factor of `a`.

    Raises
    ------
    LinAlgError : if decomposition fails.

    See Also
    --------
    cho_factor : Compute the Cholesky decomposition without explicitly setting
                    the other triangle to 0.

    Notes
    -----
    During the finiteness check (if selected), the entire matrix `a` is
    checked. During decomposition, `a` is assumed to be symmetric or Hermitian
    (as applicable), and only the half selected by option `lower` is referenced.
    Consequently, if `a` is asymmetric/non-Hermitian, `cholesky` may still
    succeed if the symmetric/Hermitian matrix represented by the selected half
    is positive definite, yet it may fail if an element in the other half is
    non-finite.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import cholesky
    >>> a = np.array([[1,-2j],[2j,5]])
    >>> L = cholesky(a, lower=True)
    >>> L
    array([[ 1.+0.j,  0.+0.j],
           [ 0.+2.j,  1.+0.j]])
    >>> L @ L.T.conj()
    array([[ 1.+0.j,  0.-2.j],
           [ 0.+2.j,  5.+0.j]])

    """
    # `clean = True` represents setting other triangle to 0.
    c = _cholesky(a, lower=lower, overwrite_a=overwrite_a, clean=True,
                check_finite=check_finite)
    return c


def cholesky(
    x: Array,
    /,
    xp: Namespace,
    *,
    upper: bool = False,
    **kwargs: object,
) -> Array:
    L = xp.linalg.cholesky(x, **kwargs)
    if upper:
        U = get_xp(xp)(matrix_transpose)(L)
        if get_xp(xp)(isdtype)(U.dtype, 'complex floating'):
            U = xp.conj(U)  # pyright: ignore[reportConstantRedefinition]
        return U
    return L


def cholesky(a, /, *, upper=False):
    """
    Cholesky decomposition.

    Return the lower or upper Cholesky decomposition, ``L * L.H`` or
    ``U.H * U``, of the square matrix ``a``, where ``L`` is lower-triangular,
    ``U`` is upper-triangular, and ``.H`` is the conjugate transpose operator
    (which is the ordinary transpose if ``a`` is real-valued). ``a`` must be
    Hermitian (symmetric if real-valued) and positive-definite. No checking is
    performed to verify whether ``a`` is Hermitian or not. In addition, only
    the lower or upper-triangular and diagonal elements of ``a`` are used.
    Only ``L`` or ``U`` is actually returned.

    Parameters
    ----------
    a : (..., M, M) array_like
        Hermitian (symmetric if all elements are real), positive-definite
        input matrix.
    upper : bool
        If ``True``, the result must be the upper-triangular Cholesky factor.
        If ``False``, the result must be the lower-triangular Cholesky factor.
        Default: ``False``.

    Returns
    -------
    L : (..., M, M) array_like
        Lower or upper-triangular Cholesky factor of `a`. Returns a matrix
        object if `a` is a matrix object.

    Raises
    ------
    LinAlgError
       If the decomposition fails, for example, if `a` is not
       positive-definite.

    See Also
    --------
    scipy.linalg.cholesky : Similar function in SciPy.
    scipy.linalg.cholesky_banded : Cholesky decompose a banded Hermitian
                                   positive-definite matrix.
    scipy.linalg.cho_factor : Cholesky decomposition of a matrix, to use in
                              `scipy.linalg.cho_solve`.

    Notes
    -----
    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    The Cholesky decomposition is often used as a fast way of solving

    .. math:: A \\mathbf{x} = \\mathbf{b}

    (when `A` is both Hermitian/symmetric and positive-definite).

    First, we solve for :math:`\\mathbf{y}` in

    .. math:: L \\mathbf{y} = \\mathbf{b},

    and then for :math:`\\mathbf{x}` in

    .. math:: L^{H} \\mathbf{x} = \\mathbf{y}.

    Examples
    --------
    >>> import numpy as np
    >>> A = np.array([[1,-2j],[2j,5]])
    >>> A
    array([[ 1.+0.j, -0.-2.j],
           [ 0.+2.j,  5.+0.j]])
    >>> L = np.linalg.cholesky(A)
    >>> L
    array([[1.+0.j, 0.+0.j],
           [0.+2.j, 1.+0.j]])
    >>> np.dot(L, L.T.conj()) # verify that L * L.H = A
    array([[1.+0.j, 0.-2.j],
           [0.+2.j, 5.+0.j]])
    >>> A = [[1,-2j],[2j,5]] # what happens if A is only array_like?
    >>> np.linalg.cholesky(A) # an ndarray object is returned
    array([[1.+0.j, 0.+0.j],
           [0.+2.j, 1.+0.j]])
    >>> # But a matrix object is returned if A is a matrix object
    >>> np.linalg.cholesky(np.matrix(A))
    matrix([[ 1.+0.j,  0.+0.j],
            [ 0.+2.j,  1.+0.j]])
    >>> # The upper-triangular Cholesky factor can also be obtained.
    >>> np.linalg.cholesky(A, upper=True)
    array([[1.-0.j, 0.-2.j],
           [0.-0.j, 1.-0.j]])

    """
    gufunc = _umath_linalg.cholesky_up if upper else _umath_linalg.cholesky_lo
    a, wrap = _makearray(a)
    _assert_stacked_square(a)
    t, result_t = _commonType(a)
    signature = 'D->D' if isComplexType(t) else 'd->d'
    with errstate(call=_raise_linalgerror_nonposdef, invalid='call',
                  over='ignore', divide='ignore', under='ignore'):
        r = gufunc(a, signature=signature)
    return wrap(r.astype(result_t, copy=False))


def cholesky(a: _ods_ir.Value[_ods_ir.RankedTensorType], *, lower: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CholeskyOp(a=a, lower=lower, results=results, loc=loc, ip=ip).result


def cholesky(a: _ods_ir.Value[_ods_ir.RankedTensorType], *, lower: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return CholeskyOp(a=a, lower=lower, results=results, loc=loc, ip=ip).result


def cholesky(x: Array, *, symmetrize_input: bool = True) -> Array:
  r"""Cholesky decomposition.

  Computes the Cholesky decomposition

  .. math::
    A = L . L^H

  of square matrices, :math:`A`, such that :math:`L`
  is lower triangular. The matrices of :math:`A` must be positive-definite and
  either Hermitian, if complex, or symmetric, if real.

  Args:
    x: A batch of square Hermitian (symmetric if real) positive-definite
      matrices with shape ``[..., n, n]``.
    symmetrize_input: If ``True``, the matrix is symmetrized before Cholesky
      decomposition by computing :math:`\frac{1}{2}(x + x^H)`. If ``False``,
      only the lower triangle of ``x`` is used; the upper triangle is ignored
      and not accessed.

  Returns:
    The Cholesky decomposition as a matrix with the same dtype as ``x`` and
    shape ``[..., n, n]``. If Cholesky decomposition fails, returns a matrix
    full of NaNs. The behavior on failure may change in the future.
  """
  if symmetrize_input:
    x = symmetrize(x)
  return _tril(cholesky_p.bind(x))


def cholesky(a: ArrayLike, *, upper: bool = False, symmetrize_input: bool = True) -> Array:
  """Compute the Cholesky decomposition of a matrix.

  JAX implementation of :func:`numpy.linalg.cholesky`.

  The Cholesky decomposition of a matrix `A` is:

  .. math::

     A = U^HU

  or

  .. math::

    A = LL^H

  where `U` is an upper-triangular matrix and `L` is a lower-triangular matrix, and
  :math:`X^H` is the Hermitian transpose of `X`.

  Args:
    a: input array, representing a (batched) positive-definite hermitian matrix.
      Must have shape ``(..., N, N)``.
    upper: if True, compute the upper Cholesky decomposition `U`. if False
      (default), compute the lower Cholesky decomposition `L`.
    symmetrize_input: if True (default) then input is symmetrized, which leads
      to better behavior under automatic differentiation. Note that when this
      is set to True, both the upper and lower triangles of the input will
      be used in computing the decomposition.

  Returns:
    array of shape ``(..., N, N)`` representing the Cholesky decomposition
    of the input. If the input is not Hermitian positive-definite, the result
    will contain NaN entries.


  See also:
    - :func:`jax.scipy.linalg.cholesky`: SciPy-style Cholesky API
    - :func:`jax.lax.linalg.cholesky`: XLA-style Cholesky API

  Examples:
    A small real Hermitian positive-definite matrix:

    >>> x = jnp.array([[2., 1.],
    ...                [1., 2.]])

    Lower Cholesky factorization:

    >>> jnp.linalg.cholesky(x)
    Array([[1.4142135 , 0.        ],
           [0.70710677, 1.2247449 ]], dtype=float32)

    Upper Cholesky factorization:

    >>> jnp.linalg.cholesky(x, upper=True)
    Array([[1.4142135 , 0.70710677],
           [0.        , 1.2247449 ]], dtype=float32)

    Reconstructing ``x`` from its factorization:

    >>> L = jnp.linalg.cholesky(x)
    >>> jnp.allclose(x, L @ L.T)
    Array(True, dtype=bool)
  """
  a = ensure_arraylike("jnp.linalg.cholesky", a)
  a, = promote_dtypes_inexact(a)
  L = lax_linalg.cholesky(a, symmetrize_input=symmetrize_input)
  return L.mT.conj() if upper else L


def cholesky(a: ArrayLike, lower: bool = False, overwrite_a: bool = False,
             check_finite: bool = True) -> Array:
  """Compute the Cholesky decomposition of a matrix.

  JAX implementation of :func:`scipy.linalg.cholesky`.

  The Cholesky decomposition of a matrix `A` is:

  .. math::

     A = U^HU = LL^H

  where `U` is an upper-triangular matrix and `L` is a lower-triangular matrix.

  Args:
    a: input array, representing a (batched) positive-definite hermitian matrix.
      Must have shape ``(..., N, N)``.
    lower: if True, compute the lower Cholesky decomposition `L`. if False
      (default), compute the upper Cholesky decomposition `U`.
    overwrite_a: unused by JAX
    check_finite: unused by JAX

  Returns:
    array of shape ``(..., N, N)`` representing the cholesky decomposition
    of the input.

  See Also:
   - :func:`jax.numpy.linalg.cholesky`: NumPy-stype Cholesky API
   - :func:`jax.lax.linalg.cholesky`: XLA-style Cholesky API
   - :func:`jax.scipy.linalg.cho_factor`
   - :func:`jax.scipy.linalg.cho_solve`

  Examples:
    A small real Hermitian positive-definite matrix:

    >>> x = jnp.array([[2., 1.],
    ...                [1., 2.]])

    Upper Cholesky factorization:

    >>> jax.scipy.linalg.cholesky(x)
    Array([[1.4142135 , 0.70710677],
           [0.        , 1.2247449 ]], dtype=float32)

    Lower Cholesky factorization:

    >>> jax.scipy.linalg.cholesky(x, lower=True)
    Array([[1.4142135 , 0.        ],
           [0.70710677, 1.2247449 ]], dtype=float32)

    Reconstructing ``x`` from its factorization:

    >>> L = jax.scipy.linalg.cholesky(x, lower=True)
    >>> jnp.allclose(x, L @ L.T)
    Array(True, dtype=bool)
  """
  del overwrite_a, check_finite  # Unused
  return _cholesky(a, lower)

