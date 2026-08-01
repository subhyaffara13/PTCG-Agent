
def companion(a):
    """
    Create a companion matrix.

    Create the companion matrix [1]_ associated with the polynomial whose
    coefficients are given in `a`.

    Array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    a : (..., N) array_like
        1-D array of polynomial coefficients. The length of `a` must be
        at least two, and ``a[0]`` must not be zero.
        M-dimensional arrays are treated as a batch: each slice along the last
        axis is a 1-D array of polynomial coefficients.

    Returns
    -------
    c : (..., N-1, N-1) ndarray
        For 1-D input, the first row of `c` is ``-a[1:]/a[0]``, and the first
        sub-diagonal is all ones.  The data-type of the array is the same
        as the data-type of ``1.0*a[0]``.
        For batch input, each slice of shape ``(N-1, N-1)`` along the last two
        dimensions of the output corresponds with a slice of shape ``(N,)``
        along the last dimension of the input.

    Raises
    ------
    ValueError
        If any of the following are true: a) ``a.shape[-1] < 2``; b) ``a[..., 0] == 0``.

    Notes
    -----
    .. versionadded:: 0.8.0

    References
    ----------
    .. [1] R. A. Horn & C. R. Johnson, *Matrix Analysis*.  Cambridge, UK:
        Cambridge University Press, 1999, pp. 146-7.

    Examples
    --------
    >>> from scipy.linalg import companion
    >>> companion([1, -10, 31, -30])
    array([[ 10., -31.,  30.],
           [  1.,   0.,   0.],
           [  0.,   1.,   0.]])

    """
    a = np.atleast_1d(a)
    n = a.shape[-1]

    if n < 2:
        raise ValueError("The length of `a` along the last axis must be at least 2.")

    if np.any(a[..., 0] == 0):
        raise ValueError("The first coefficient(s) of `a` (i.e. elements "
                         "of `a[..., 0]`) must not be zero.")

    first_row = -a[..., 1:] / (1.0 * a[..., 0:1])
    c = np.zeros(a.shape[:-1] + (n - 1, n - 1), dtype=first_row.dtype)
    c[..., 0, :] = first_row
    c[..., np.arange(1, n - 1), np.arange(0, n - 2)] = 1
    return c


def companion(a: ArrayLike) -> Array:
  r"""Construct a companion matrix.

  JAX implementation of :func:`scipy.linalg.companion`.

  Given polynomial coefficients :math:`a = [a_0, a_1, \ldots, a_{n-1}]` with
  :math:`a_0 \neq 0`, the companion matrix is the :math:`(n-1) \times (n-1)`
  matrix whose first row is :math:`-[a_1, a_2, \ldots, a_{n-1}] / a_0` and
  whose first sub-diagonal is filled with ones.

  Args:
    a: array of shape ``(..., N)`` with ``N >= 2`` specifying the polynomial
      coefficients.

  Returns:
    A companion matrix of shape ``(..., N - 1, N - 1)``.

  Note:
    Unlike :func:`scipy.linalg.companion`, this function does not check at
    runtime that ``a[..., 0]`` is non-zero; if the leading coefficient is
    zero, the result will contain ``inf`` or ``nan`` entries.

  Examples:
    >>> jax.scipy.linalg.companion(jnp.array([1., -10., 31., -30.]))
    Array([[ 10., -31.,  30.],
           [  1.,   0.,   0.],
           [  0.,   1.,   0.]], dtype=float32)
  """
  a, = promote_args_inexact("companion", a)
  a = jnp.atleast_1d(a)
  if a.shape[-1] < 2:
    raise ValueError(
        "The length of `a` along the last axis must be at least 2; "
        f"got shape {a.shape}.")
  return _companion(a)

