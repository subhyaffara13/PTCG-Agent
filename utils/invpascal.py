
def invpascal(n, kind='symmetric', exact=True):
    """
    Returns the inverse of the n x n Pascal matrix.

    The Pascal matrix is a matrix containing the binomial coefficients as
    its elements.

    Parameters
    ----------
    n : int
        The size of the matrix to create; that is, the result is an n x n
        matrix.
    kind : str, optional
        Must be one of 'symmetric', 'lower', or 'upper'.
        Default is 'symmetric'.
    exact : bool, optional
        If `exact` is True, the result is either an array of type
        ``numpy.int64`` (if `n` <= 35) or an object array of Python integers.
        If `exact` is False, the coefficients in the matrix are computed using
        `scipy.special.comb` with `exact=False`. The result will be a floating
        point array, and for large `n`, the values in the array will not be the
        exact coefficients.

    Returns
    -------
    invp : (n, n) ndarray
        The inverse of the Pascal matrix.

    See Also
    --------
    pascal

    Notes
    -----

    .. versionadded:: 0.16.0

    References
    ----------
    .. [1] "Pascal matrix", https://en.wikipedia.org/wiki/Pascal_matrix
    .. [2] Cohen, A. M., "The inverse of a Pascal matrix", Mathematical
           Gazette, 59(408), pp. 111-112, 1975.

    Examples
    --------
    >>> from scipy.linalg import invpascal, pascal
    >>> invp = invpascal(5)
    >>> invp
    array([[  5, -10,  10,  -5,   1],
           [-10,  30, -35,  19,  -4],
           [ 10, -35,  46, -27,   6],
           [ -5,  19, -27,  17,  -4],
           [  1,  -4,   6,  -4,   1]])

    >>> p = pascal(5)
    >>> p.dot(invp)
    array([[ 1.,  0.,  0.,  0.,  0.],
           [ 0.,  1.,  0.,  0.,  0.],
           [ 0.,  0.,  1.,  0.,  0.],
           [ 0.,  0.,  0.,  1.,  0.],
           [ 0.,  0.,  0.,  0.,  1.]])

    An example of the use of `kind` and `exact`:

    >>> invpascal(5, kind='lower', exact=False)
    array([[ 1., -0.,  0., -0.,  0.],
           [-1.,  1., -0.,  0., -0.],
           [ 1., -2.,  1., -0.,  0.],
           [-1.,  3., -3.,  1., -0.],
           [ 1., -4.,  6., -4.,  1.]])

    """
    from scipy.special import comb

    if kind not in ['symmetric', 'lower', 'upper']:
        raise ValueError("'kind' must be 'symmetric', 'lower' or 'upper'.")

    if kind == 'symmetric':
        if exact:
            if n > 34:
                dt = object
            else:
                dt = np.int64
        else:
            dt = np.float64
        invp = np.empty((n, n), dtype=dt)
        for i in range(n):
            for j in range(0, i + 1):
                v = 0
                for k in range(n - i):
                    v += comb(i + k, k, exact=exact) * comb(i + k, i + k - j,
                                                            exact=exact)
                invp[i, j] = (-1)**(i - j) * v
                if i != j:
                    invp[j, i] = invp[i, j]
    else:
        # For the 'lower' and 'upper' cases, we computer the inverse by
        # changing the sign of every other diagonal of the pascal matrix.
        invp = pascal(n, kind=kind, exact=exact)
        if invp.dtype == np.uint64:
            # This cast from np.uint64 to int64 OK, because if `kind` is not
            # "symmetric", the values in invp are all much less than 2**63.
            invp = invp.view(np.int64)

        # The toeplitz matrix has alternating bands of 1 and -1.
        invp *= toeplitz((-1)**np.arange(n)).astype(invp.dtype)

    return invp


def invpascal(n: int, kind: str | None = None) -> Array:
  r"""Compute the inverse of the Pascal matrix of order n.

  JAX implementation of :func:`scipy.linalg.invpascal`.

  The inverses of the lower and upper Pascal matrices have a simple closed
  form,

  .. math::

     L^{-1}_{ij} = (-1)^{i - j} \binom{i}{j}, \qquad U^{-1} = (L^{-1})^T,

  and the symmetric inverse satisfies :math:`P_S^{-1} = U^{-1} L^{-1}`.

  Args:
    n: the size of the matrix to create.
    kind: (optional) must be one of ``lower``, ``upper``, or ``symmetric``
      (default).

  Returns:
    The inverse of the Pascal matrix of shape ``(n, n)``.

  Note:
    Unlike :func:`scipy.linalg.invpascal`, this function does not support
    ``exact=True``. The entries are computed in floating point through
    :func:`~jax.scipy.special.gammaln`-based binomial coefficients.

  See Also:
    :func:`jax.scipy.linalg.pascal`

  Examples:
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   print(jax.scipy.linalg.invpascal(4, kind="lower"))
    ...   print(jax.scipy.linalg.invpascal(5))
    [[ 1. -0.  0. -0.]
     [-1.  1. -0.  0.]
     [ 1. -2.  1. -0.]
     [-1.  3. -3.  1.]]
    [[  5. -10.  10.  -5.   1.]
     [-10.  30. -35.  19.  -4.]
     [ 10. -35.  46. -27.   6.]
     [ -5.  19. -27.  17.  -4.]
     [  1.  -4.   6.  -4.   1.]]
  """
  if kind is None:
    kind = "symmetric"

  valid_kind = ["symmetric", "lower", "upper"]
  if kind not in valid_kind:
    raise ValueError(f"Expected kind to be one of: {valid_kind}; got {kind}")

  a = jnp.arange(n, dtype=dtypes.default_float_dtype())
  i = a[:, None]
  j = a[None, :]
  # Lower-triangular inverse: (-1)^(i-j) * binom(i, j).
  L_inv = ((-1.0) ** (i - j)) * _binom(i, j)

  if kind == "lower":
    return L_inv
  if kind == "upper":
    return L_inv.T
  return jnp.dot(L_inv.T, L_inv)

