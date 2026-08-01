
def matrix_rank(input, tol=None, symmetric=False, *, out=None) -> Tensor:
    raise RuntimeError(
        "This function was deprecated since version 1.9 and is now removed.\n"
        "Please use the `torch.linalg.matrix_rank` function instead. "
        "The parameter 'symmetric' was renamed in `torch.linalg.matrix_rank()` to 'hermitian'."
    )


def matrix_rank(a: ArrayLike, tol=None, hermitian=False):
    a = _atleast_float_1(a)

    if a.ndim < 2:
        return int((a != 0).any())

    if tol is None:
        # follow https://github.com/numpy/numpy/blob/v1.24.0/numpy/linalg/linalg.py#L1885
        atol = 0
        rtol = max(a.shape[-2:]) * torch.finfo(a.dtype).eps
    else:
        atol, rtol = tol, 0
    return torch.linalg.matrix_rank(a, atol=atol, rtol=rtol, hermitian=hermitian)


def matrix_rank(
    x: Array,
    /,
    xp: Namespace,
    *,
    rtol: float | Array | None = None,
    **kwargs: object,
) -> Array:
    # this is different from xp.linalg.matrix_rank, which supports 1
    # dimensional arrays.
    if x.ndim < 2:
        raise xp.linalg.LinAlgError("1-dimensional array given. Array must be at least two-dimensional")
    S: Array = get_xp(xp)(svdvals)(x, **kwargs)
    if rtol is None:
        tol = S.max(axis=-1, keepdims=True) * max(x.shape[-2:]) * xp.finfo(S.dtype).eps
    else:
        # this is different from xp.linalg.matrix_rank, which does not
        # multiply the tolerance by the largest singular value.
        tol = S.max(axis=-1, keepdims=True)*xp.asarray(rtol)[..., xp.newaxis]
    return xp.count_nonzero(S > tol, axis=-1)


def matrix_rank(A, tol=None, hermitian=False, *, rtol=None):
    """
    Return matrix rank of array using SVD method

    Rank of the array is the number of singular values of the array that are
    greater than `tol`.

    Parameters
    ----------
    A : {(M,), (..., M, N)} array_like
        Input vector or stack of matrices.
    tol : (...) array_like, float, optional
        Threshold below which SVD values are considered zero. If `tol` is
        None, and ``S`` is an array with singular values for `M`, and
        ``eps`` is the epsilon value for datatype of ``S``, then `tol` is
        set to ``S.max() * max(M, N) * eps``.
    hermitian : bool, optional
        If True, `A` is assumed to be Hermitian (symmetric if real-valued),
        enabling a more efficient method for finding singular values.
        Defaults to False.
    rtol : (...) array_like, float, optional
        Parameter for the relative tolerance component. Only ``tol`` or
        ``rtol`` can be set at a time. Defaults to ``max(M, N) * eps``.

        .. versionadded:: 2.0.0

    Returns
    -------
    rank : (...) array_like
        Rank of A.

    Notes
    -----
    The default threshold to detect rank deficiency is a test on the magnitude
    of the singular values of `A`.  By default, we identify singular values
    less than ``S.max() * max(M, N) * eps`` as indicating rank deficiency
    (with the symbols defined above). This is the algorithm MATLAB uses [1]_.
    It also appears in *Numerical recipes* in the discussion of SVD solutions
    for linear least squares [2]_.

    This default threshold is designed to detect rank deficiency accounting
    for the numerical errors of the SVD computation. Imagine that there
    is a column in `A` that is an exact (in floating point) linear combination
    of other columns in `A`. Computing the SVD on `A` will not produce
    a singular value exactly equal to 0 in general: any difference of
    the smallest SVD value from 0 will be caused by numerical imprecision
    in the calculation of the SVD. Our threshold for small SVD values takes
    this numerical imprecision into account, and the default threshold will
    detect such numerical rank deficiency. The threshold may declare a matrix
    `A` rank deficient even if the linear combination of some columns of `A`
    is not exactly equal to another column of `A` but only numerically very
    close to another column of `A`.

    We chose our default threshold because it is in wide use. Other thresholds
    are possible.  For example, elsewhere in the 2007 edition of *Numerical
    recipes* there is an alternative threshold of ``S.max() *
    np.finfo(A.dtype).eps / 2. * np.sqrt(m + n + 1.)``. The authors describe
    this threshold as being based on "expected roundoff error" (p 71).

    The thresholds above deal with floating point roundoff error in the
    calculation of the SVD.  However, you may have more information about
    the sources of error in `A` that would make you consider other tolerance
    values to detect *effective* rank deficiency. The most useful measure
    of the tolerance depends on the operations you intend to use on your
    matrix. For example, if your data come from uncertain measurements with
    uncertainties greater than floating point epsilon, choosing a tolerance
    near that uncertainty may be preferable. The tolerance may be absolute
    if the uncertainties are absolute rather than relative.

    References
    ----------
    .. [1] MATLAB reference documentation, "Rank"
           https://www.mathworks.com/help/techdoc/ref/rank.html
    .. [2] W. H. Press, S. A. Teukolsky, W. T. Vetterling and B. P. Flannery,
           "Numerical Recipes (3rd edition)", Cambridge University Press, 2007,
           page 795.

    Examples
    --------
    >>> import numpy as np
    >>> from numpy.linalg import matrix_rank
    >>> matrix_rank(np.eye(4)) # Full rank matrix
    4
    >>> I=np.eye(4); I[-1,-1] = 0. # rank deficient matrix
    >>> matrix_rank(I)
    3
    >>> matrix_rank(np.ones((4,))) # 1 dimension - rank 1 unless all 0
    1
    >>> matrix_rank(np.zeros((4,)))
    0
    """
    if rtol is not None and tol is not None:
        raise ValueError("`tol` and `rtol` can't be both set.")

    A = asarray(A)
    if A.ndim < 2:
        return int(not all(A == 0))

    S = svd(A, compute_uv=False, hermitian=hermitian)

    if tol is None:
        if rtol is None:
            rtol = max(A.shape[-2:]) * finfo(S.dtype).eps
        else:
            rtol = asarray(rtol)[..., newaxis]
        tol = S.max(axis=-1, keepdims=True, initial=0) * rtol
    else:
        tol = asarray(tol)[..., newaxis]

    return count_nonzero(S > tol, axis=-1)


def matrix_rank(
  M: ArrayLike, rtol: ArrayLike | None = None,
  *, hermitian: bool = False, tol: ArrayLike | None = None) -> Array:
  """Compute the rank of a matrix.

  JAX implementation of :func:`numpy.linalg.matrix_rank`.

  The rank is calculated via the Singular Value Decomposition (SVD), and determined
  by the number of singular values greater than the specified tolerance.

  Args:
    M: array of shape ``(..., N, K)`` whose rank is to be computed.
    rtol: optional array of shape ``(...)`` specifying the tolerance. Singular values
      smaller than `rtol * largest_singular_value` are considered to be zero. If
      ``rtol`` is None (the default), a reasonable default is chosen based the
      floating point precision of the input.
    hermitian: if True, then the input is assumed to be Hermitian, and a more
      efficient algorithm is used (default: False)
    tol: alias of the ``rtol`` argument present for backward compatibility.
      Only one of `rtol` or `tol` may be specified.

  Returns:
    array of shape ``a.shape[-2]`` giving the matrix rank.

  Notes:
    The rank calculation may be inaccurate for matrices with very small singular
    values or those that are numerically ill-conditioned. Consider adjusting the
    ``rtol`` parameter or using a more specialized rank computation method in such cases.

  Examples:
    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> jnp.linalg.matrix_rank(a)
    Array(2, dtype=int32)

    >>> b = jnp.array([[1, 0],  # Rank-deficient matrix
    ...                [0, 0]])
    >>> jnp.linalg.matrix_rank(b)
    Array(1, dtype=int32)
  """
  M = ensure_arraylike("jnp.linalg.matrix_rank", M)
  if tol is not None:
    if rtol is not None:
      raise ValueError("matrix_rank: only one of tol or rtol may be specified.")
    rtol = tol
  del tol
  M, = promote_dtypes_inexact(M)
  if M.ndim < 2:
    return (M != 0).any().astype(np.int32)
  S = svd(M, full_matrices=False, compute_uv=False, hermitian=hermitian)
  if rtol is None:
    rtol = S.max(-1) * np.max(M.shape[-2:]).astype(S.dtype) * jnp.finfo(S.dtype).eps
  rtol = jnp.expand_dims(rtol, np.ndim(rtol))
  return reductions.sum(S > rtol, axis=-1)

