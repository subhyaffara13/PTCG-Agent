
def helmert(n, full=False):
    """
    Create a Helmert matrix of order `n`.

    This has applications in statistics, compositional or simplicial analysis,
    and in Aitchison geometry.

    Parameters
    ----------
    n : int
        The size of the array to create.
    full : bool, optional
        If True the (n, n) ndarray will be returned.
        Otherwise the submatrix that does not include the first
        row will be returned.
        Default: False.

    Returns
    -------
    M : ndarray
        The Helmert matrix.
        The shape is (n, n) or (n-1, n) depending on the `full` argument.

    Examples
    --------
    >>> from scipy.linalg import helmert
    >>> helmert(5, full=True)
    array([[ 0.4472136 ,  0.4472136 ,  0.4472136 ,  0.4472136 ,  0.4472136 ],
           [ 0.70710678, -0.70710678,  0.        ,  0.        ,  0.        ],
           [ 0.40824829,  0.40824829, -0.81649658,  0.        ,  0.        ],
           [ 0.28867513,  0.28867513,  0.28867513, -0.8660254 ,  0.        ],
           [ 0.2236068 ,  0.2236068 ,  0.2236068 ,  0.2236068 , -0.89442719]])

    """
    H = np.tril(np.ones((n, n)), -1) - np.diag(np.arange(n))
    d = np.arange(n) * np.arange(1, n+1)
    H[0] = 1
    d[0] = n
    H_full = H / np.sqrt(d)[:, np.newaxis]
    if full:
        return H_full
    else:
        return H_full[1:]


def helmert(n: int, full: bool = False) -> Array:
  r"""Construct a Helmert matrix.

  JAX implementation of :func:`scipy.linalg.helmert`.

  The Helmert matrix has rows of orthonormal contrasts. For ``k = 1, ...,
  n - 1``, row ``k - 1`` is :math:`(\underbrace{1, \ldots, 1}_{k}, -k, 0,
  \ldots, 0) / \sqrt{k(k + 1)}`. If ``full`` is ``True``, a row of
  :math:`1 / \sqrt{n}` is prepended.

  Args:
    n: size of the matrix. Must be a positive integer.
    full: if ``True``, return the full ``(n, n)`` matrix; otherwise return
      only the ``(n - 1, n)`` contrast block. Defaults to ``False``.

  Returns:
    A Helmert matrix of shape ``(n - 1, n)`` if ``full`` is ``False``, or
    ``(n, n)`` if ``full`` is ``True``.

  Examples:
    >>> jax.scipy.linalg.helmert(2, full=True).round(3)
    Array([[ 0.707,  0.707],
           [ 0.707, -0.707]], dtype=float32)
  """
  if n < 1:
    raise ValueError(f"n must be a positive integer; got {n}.")
  i = jnp.arange(n - 1)[:, None]
  j = jnp.arange(n)[None, :]
  k = i + 1
  k_f = k.astype(dtypes.default_float_dtype())
  denom = jnp.sqrt(k_f * (k_f + 1))
  H = jnp.where(j <= i, 1.0 / denom,
                jnp.where(j == k, -k_f / denom, jnp.zeros_like(denom)))
  if full:
    first_row = jnp.full((1, n), 1.0 / jnp.sqrt(n), dtype=H.dtype)
    H = jnp.concatenate([first_row, H], axis=0)
  return H

