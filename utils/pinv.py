
def pinv(a: ArrayLike, rcond=1e-15, hermitian=False):
    a = _atleast_float_1(a)
    return torch.linalg.pinv(a, rtol=rcond, hermitian=hermitian)


def pinv(a, *, atol=None, rtol=None, return_rank=False, check_finite=True):
    """
    Compute the (Moore-Penrose) pseudo-inverse of a matrix.

    Calculate a generalized inverse of a matrix using its
    singular-value decomposition ``U @ S @ V`` in the economy mode and picking
    up only the columns/rows that are associated with significant singular
    values.

    If ``s`` is the maximum singular value of ``a``, then the
    significance cut-off value is determined by ``atol + rtol * s``. Any
    singular value below this value is assumed insignificant.

    The `a` array argument may have additional "batch" dimensions prepended to the core
    shape. In this case, the array is treated as a batch of lower-dimensional slices;
    see :ref:`linalg_batch` for details.

    Parameters
    ----------
    a : (..., M, N) array_like
        Matrix to be pseudo-inverted.
    atol : float, optional
        Absolute threshold term, default value is 0.

        .. versionadded:: 1.7.0

    rtol : float, optional
        Relative threshold term, default value is ``max(M, N) * eps`` where
        ``eps`` is the machine precision value of the datatype of ``a``.

        .. versionadded:: 1.7.0

    return_rank : bool, optional
        If True, return the effective rank of the matrix.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    B : (..., N, M) ndarray
        The pseudo-inverse of matrix `a`.
    rank : int
        The effective rank of the matrix. Returned if `return_rank` is True.

    Raises
    ------
    LinAlgError
        If SVD computation does not converge.

    See Also
    --------
    pinvh : Moore-Penrose pseudoinverse of a hermitian matrix.

    Notes
    -----
    If ``A`` is invertible then the Moore-Penrose pseudoinverse is exactly
    the inverse of ``A`` [1]_. If ``A`` is not invertible then the
    Moore-Penrose pseudoinverse computes the ``x`` solution to ``Ax = b`` such
    that ``||Ax - b||`` is minimized [1]_.

    References
    ----------
    .. [1] Penrose, R. (1956). On best approximate solutions of linear matrix
           equations. Mathematical Proceedings of the Cambridge Philosophical
           Society, 52(1), 17-19. :doi:`10.1017/S0305004100030929`.

    Examples
    --------

    Given an ``m x n`` matrix ``A`` and an ``n x m`` matrix ``B`` the four
    Moore-Penrose conditions are:

    1. ``ABA = A`` (``B`` is a generalized inverse of ``A``),
    2. ``BAB = B`` (``A`` is a generalized inverse of ``B``),
    3. ``(AB)* = AB`` (``AB`` is hermitian),
    4. ``(BA)* = BA`` (``BA`` is hermitian) [1]_.

    Here, ``A*`` denotes the conjugate transpose. The Moore-Penrose
    pseudoinverse is a unique ``B`` that satisfies all four of these
    conditions and exists for any ``A``. Note that, unlike the standard
    matrix inverse, ``A`` does not have to be a square matrix or have
    linearly independent columns/rows.

    As an example, we can calculate the Moore-Penrose pseudoinverse of a
    random non-square matrix and verify it satisfies the four conditions.

    >>> import numpy as np
    >>> from scipy import linalg
    >>> rng = np.random.default_rng()
    >>> A = rng.standard_normal((9, 6))
    >>> B = linalg.pinv(A)
    >>> np.allclose(A @ B @ A, A)  # Condition 1
    True
    >>> np.allclose(B @ A @ B, B)  # Condition 2
    True
    >>> np.allclose((A @ B).conj().T, A @ B)  # Condition 3
    True
    >>> np.allclose((B @ A).conj().T, B @ A)  # Condition 4
    True

    If the input array has more than two dimensions, it is interpreted as a batch of
    two-dimensional slices:

    >>> a = np.stack((np.zeros((3, 3)), np.eye(3)))
    >>> p, ranks = linalg.pinv(a, return_rank=True)
    >>> p.shape
    (2, 3, 3)
    >>> ranks
    array([0, 3])
    """
    a = _asarray_validated(a, check_finite=check_finite)
    u, s, vh = _decomp_svd.svd(a.conj(), full_matrices=False, check_finite=False)

    atol = 0. if atol is None else atol
    rtol = max(a.shape[-2:]) * np.finfo(u.dtype).eps if (rtol is None) else rtol
    if (atol < 0.) or (rtol < 0.):
        raise ValueError("atol and rtol values must be positive.")

    maxS = np.max(s, axis=-1, initial=0., keepdims=True)
    val = atol + maxS * rtol

    large = s > val
    rank = np.sum(large, axis=-1)

    # zero out small singular values, 1/s large singular values
    np.divide(1, s, where=large, out=s)
    s[~large] = 0

    B = vh.mT @ (s[..., None] * u.mT)

    if return_rank:
        return B, rank
    else:
        return B


def pinv(
    x: Array,
    /,
    xp: Namespace,
    *,
    rtol: float | Array | None = None,
    **kwargs: object,
) -> Array:
    # this is different from xp.linalg.pinv, which does not multiply the
    # default tolerance by max(M, N).
    if rtol is None:
        rtol = max(x.shape[-2:]) * xp.finfo(x.dtype).eps
    return xp.linalg.pinv(x, rcond=rtol, **kwargs)


def pinv(a, rcond=None, hermitian=False, *, rtol=_NoValue):
    """
    Compute the (Moore-Penrose) pseudo-inverse of a matrix.

    Calculate the generalized inverse of a matrix using its
    singular-value decomposition (SVD) and including all
    *large* singular values.

    Parameters
    ----------
    a : (..., M, N) array_like
        Matrix or stack of matrices to be pseudo-inverted.
    rcond : (...) array_like of float, optional
        Cutoff for small singular values.
        Singular values less than or equal to
        ``rcond * largest_singular_value`` are set to zero.
        Broadcasts against the stack of matrices. Default: ``1e-15``.
    hermitian : bool, optional
        If True, `a` is assumed to be Hermitian (symmetric if real-valued),
        enabling a more efficient method for finding singular values.
        Defaults to False.
    rtol : (...) array_like of float, optional
        Same as `rcond`, but it's an Array API compatible parameter name.
        Only `rcond` or `rtol` can be set at a time. If none of them are
        provided then NumPy's ``1e-15`` default is used. If ``rtol=None``
        is passed then the API standard default is used.

        .. versionadded:: 2.0.0

    Returns
    -------
    B : (..., N, M) ndarray
        The pseudo-inverse of `a`. If `a` is a `matrix` instance, then so
        is `B`.

    Raises
    ------
    LinAlgError
        If the SVD computation does not converge.

    See Also
    --------
    scipy.linalg.pinv : Similar function in SciPy.
    scipy.linalg.pinvh : Compute the (Moore-Penrose) pseudo-inverse of a
                         Hermitian matrix.

    Notes
    -----
    The pseudo-inverse of a matrix A, denoted :math:`A^+`, is
    defined as: "the matrix that 'solves' [the least-squares problem]
    :math:`Ax = b`," i.e., if :math:`\\bar{x}` is said solution, then
    :math:`A^+` is that matrix such that :math:`\\bar{x} = A^+b`.

    It can be shown that if :math:`Q_1 \\Sigma Q_2^T = A` is the singular
    value decomposition of A, then
    :math:`A^+ = Q_2 \\Sigma^+ Q_1^T`, where :math:`Q_{1,2}` are
    orthogonal matrices, :math:`\\Sigma` is a diagonal matrix consisting
    of A's so-called singular values, (followed, typically, by
    zeros), and then :math:`\\Sigma^+` is simply the diagonal matrix
    consisting of the reciprocals of A's singular values
    (again, followed by zeros). [1]_

    References
    ----------
    .. [1] G. Strang, *Linear Algebra and Its Applications*, 2nd Ed., Orlando,
           FL, Academic Press, Inc., 1980, pp. 139-142.

    Examples
    --------
    The following example checks that ``a * a+ * a == a`` and
    ``a+ * a * a+ == a+``:

    >>> import numpy as np
    >>> rng = np.random.default_rng()
    >>> a = rng.normal(size=(9, 6))
    >>> B = np.linalg.pinv(a)
    >>> np.allclose(a, np.dot(a, np.dot(B, a)))
    True
    >>> np.allclose(B, np.dot(B, np.dot(a, B)))
    True

    """
    a, wrap = _makearray(a)
    if rcond is None:
        if rtol is _NoValue:
            rcond = 1e-15
        elif rtol is None:
            rcond = max(a.shape[-2:]) * finfo(a.dtype).eps
        else:
            rcond = rtol
    elif rtol is not _NoValue:
        raise ValueError("`rtol` and `rcond` can't be both set.")
    else:
        # NOTE: Deprecate `rcond` in a few versions.
        pass

    rcond = asarray(rcond)
    if _is_empty_2d(a):
        m, n = a.shape[-2:]
        res = empty(a.shape[:-2] + (n, m), dtype=a.dtype)
        return wrap(res)
    a = a.conjugate()
    u, s, vt = svd(a, full_matrices=False, hermitian=hermitian)

    # discard small singular values
    cutoff = rcond[..., newaxis] * amax(s, axis=-1, keepdims=True)
    large = s > cutoff
    s = divide(1, s, where=large, out=s)
    s[~large] = 0

    res = matmul(transpose(vt), multiply(s[..., newaxis], transpose(u)))
    return wrap(res)


def pinv(a: ArrayLike, rtol: ArrayLike | None = None,
         hermitian: bool = False, *, rcond: ArrayLike | None = None) -> Array:
  """Compute the (Moore-Penrose) pseudo-inverse of a matrix.

  JAX implementation of :func:`numpy.linalg.pinv`.

  Args:
    a: array of shape ``(..., M, N)`` containing matrices to pseudo-invert.
    rtol: float or array_like of shape ``a.shape[:-2]``. Specifies the cutoff
      for small singular values.of shape ``(...,)``.
      Cutoff for small singular values; singular values smaller
      ``rtol * largest_singular_value`` are treated as zero. The default is
      determined based on the floating point precision of the dtype.
    hermitian: if True, then the input is assumed to be Hermitian, and a more
      efficient algorithm is used (default: False)
    rcond: alias of the `rtol` argument, present for backward compatibility.
      Only one of `rtol` and `rcond` may be specified.

  Returns:
    An array of shape ``(..., N, M)`` containing the pseudo-inverse of ``a``.

  See also:
    - :func:`jax.numpy.linalg.inv`: multiplicative inverse of a square matrix.

  Notes:
    :func:`jax.numpy.linalg.pinv` differs from :func:`numpy.linalg.pinv` in the
    default value of `rcond``: in NumPy, the default  is `1e-15`. In JAX, the
    default is ``10. * max(num_rows, num_cols) * jnp.finfo(dtype).eps``.

  Examples:
    >>> a = jnp.array([[1, 2],
    ...                [3, 4],
    ...                [5, 6]])
    >>> a_pinv = jnp.linalg.pinv(a)
    >>> a_pinv  # doctest: +SKIP
    Array([[-1.333332  , -0.33333257,  0.6666657 ],
           [ 1.0833322 ,  0.33333272, -0.41666582]], dtype=float32)

    The pseudo-inverse operates as a multiplicative inverse so long as the
    output is not rank-deficient:

    >>> jnp.allclose(a_pinv @ a, jnp.eye(2), atol=1E-4)
    Array(True, dtype=bool)
  """
  if rcond is not None:
    if rtol is not None:
      raise ValueError("pinv: only one of rtol and rcond may be specified.")
    rtol = rcond
  del rcond
  return _pinv(a, rtol, hermitian)

