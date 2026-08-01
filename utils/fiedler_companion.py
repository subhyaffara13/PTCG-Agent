
def fiedler_companion(a):
    """Returns a Fiedler companion matrix.

    Given a polynomial coefficient array ``a``, this function forms a
    pentadiagonal matrix with a special structure whose eigenvalues coincides
    with the roots of ``a``.

    Array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    a : (..., N) array_like
        1-D array of polynomial coefficients in descending order with a nonzero
        leading coefficient. For ``N < 2``, an empty array is returned.
        N-dimensional arrays are treated as a batch: each slice along the last
        axis is a 1-D array of polynomial coefficients.

    Returns
    -------
    c : (..., N-1, N-1) ndarray
        Resulting companion matrix. For batch input, each slice of shape
        ``(N-1, N-1)`` along the last two dimensions of the output corresponds
        with a slice of shape ``(N,)`` along the last dimension of the input.

    See Also
    --------
    companion

    Notes
    -----
    Similar to `companion`, each leading coefficient along the last axis of the
    input should be nonzero.
    If the leading coefficient is not 1, other coefficients are rescaled before
    the array generation. To avoid numerical issues, it is best to provide a
    monic polynomial.

    .. versionadded:: 1.3.0

    References
    ----------
    .. [1] M. Fiedler, " A note on companion matrices", Linear Algebra and its
        Applications, 2003, :doi:`10.1016/S0024-3795(03)00548-2`

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import fiedler_companion, eigvals
    >>> p = np.poly(np.arange(1, 9, 2))  # [1., -16., 86., -176., 105.]
    >>> fc = fiedler_companion(p)
    >>> fc
    array([[  16.,  -86.,    1.,    0.],
           [   1.,    0.,    0.,    0.],
           [   0.,  176.,    0., -105.],
           [   0.,    1.,    0.,    0.]])
    >>> eigvals(fc)
    array([7.+0.j, 5.+0.j, 3.+0.j, 1.+0.j])

    """
    a = np.atleast_1d(a)

    if a.ndim > 1:
        return np.apply_along_axis(fiedler_companion, -1, a)

    if a.size <= 2:
        if a.size == 2:
            return np.array([[-(a/a[0])[-1]]])
        if a.size == 1:
            return np.empty((0, 0), dtype=a.dtype)
        return np.array([], dtype=a.dtype)

    if a[0] == 0.:
        raise ValueError('Leading coefficient is zero.')

    a = a/a[0]
    n = a.size - 1
    c = np.zeros((n, n), dtype=a.dtype)
    # subdiagonals
    c[range(3, n, 2), range(1, n-2, 2)] = 1.
    c[range(2, n, 2), range(1, n-1, 2)] = -a[3::2]
    # superdiagonals
    c[range(0, n-2, 2), range(2, n, 2)] = 1.
    c[range(0, n-1, 2), range(1, n, 2)] = -a[2::2]
    c[[0, 1], 0] = [-a[1], 1]

    return c


def fiedler_companion(a: ArrayLike) -> Array:
  r"""Construct a Fiedler companion matrix.

  JAX implementation of :func:`scipy.linalg.fiedler_companion`.

  Given polynomial coefficients :math:`a = [a_0, a_1, \ldots, a_{n}]` with
  :math:`a_0 \neq 0`, this constructs a pentadiagonal matrix whose
  eigenvalues coincide with the roots of the polynomial. The result is
  similar to :func:`companion` but with a sparser, banded structure.

  Args:
    a: array of shape ``(..., N)`` specifying the polynomial coefficients in
      descending order. The last axis must have nonzero length. For ``N == 1``
      an empty ``(0, 0)`` matrix is returned along that slice.

  Raises:
    ValueError: if the last axis of ``a`` has length zero.

  Returns:
    A Fiedler companion matrix of shape ``(..., N - 1, N - 1)``.

  Note:
    Unlike :func:`scipy.linalg.fiedler_companion`, this function does not
    check at runtime that ``a[..., 0]`` is non-zero; if the leading
    coefficient is zero, the result will contain ``inf`` or ``nan`` entries.

  Examples:
    >>> a = jnp.array([1., -16., 86., -176., 105.])
    >>> jax.scipy.linalg.fiedler_companion(a)
    Array([[ 16., -86.,   1.,   0.],
           [  1.,   0.,   0.,   0.],
           [  0., 176.,   0., -105.],
           [  0.,   1.,   0.,   0.]], dtype=float32)
  """
  a, = promote_args_inexact("fiedler_companion", a)
  a = jnp.atleast_1d(a)
  if a.shape[-1] == 0:
    raise ValueError(
        "fiedler_companion requires the last axis of 'a' to have nonzero "
        f"length, but got an array of shape {a.shape}.")
  return _fiedler_companion(a)

