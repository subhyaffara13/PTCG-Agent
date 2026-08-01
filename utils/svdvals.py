
def svdvals(A: TensorLikeType) -> Tensor:
    return svd(A, full_matrices=False)[1]


def svdvals(a, overwrite_a=False, check_finite=True):
    """
    Compute singular values of a matrix.

    Parameters
    ----------
    a : (M, N) array_like
        Matrix to decompose.
    overwrite_a : bool, optional
        Whether to overwrite data in `a` (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    s : (min(M, N),) ndarray
        The singular values, sorted in decreasing order.

    Raises
    ------
    LinAlgError
        If SVD computation does not converge.

    See Also
    --------
    svd : Compute the full singular value decomposition of a matrix.
    diagsvd : Construct the Sigma matrix, given the vector s.

    Notes
    -----
    Array argument of this function, `a`, may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import svdvals
    >>> m = np.array([[1.0, 0.0],
    ...               [2.0, 3.0],
    ...               [1.0, 1.0],
    ...               [0.0, 2.0],
    ...               [1.0, 0.0]])
    >>> svdvals(m)
    array([ 4.28091555,  1.63516424])

    If the input matrix has more than two dimensions, it is interpreted as a batch of
    two-dimensional matrices:

    >>> mm = np.stack((m, 2*m))
    >>> svdvals(mm)
    array([[4.28091555, 1.63516424],
           [8.56183109, 3.27032847]])

    We can verify the maximum singular value of `m` by computing the maximum
    length of `m @ u` over all the unit vectors `u` in the (x,y) plane.
    We approximate "all" the unit vectors with a large sample. Because
    of linearity, we only need the unit vectors with angles in ``[0, pi]``.

    >>> t = np.linspace(0, np.pi, 2000)
    >>> u = np.array([np.cos(t), np.sin(t)])
    >>> np.linalg.norm(m @ u, axis=0).max()
    4.2809152422538475

    `p` is a projection matrix with rank 1. With exact arithmetic,
    its singular values would be ``[1, 0, 0, 0]``.

    >>> v = np.array([0.1, 0.3, 0.9, 0.3])
    >>> p = np.outer(v, v)
    >>> svdvals(p)
    array([  1.00000000e+00,   2.02021698e-17,   1.56692500e-17,
             8.15115104e-34])

    The singular values of an orthogonal matrix are all 1. Here, we
    create a random orthogonal matrix by using the ``rvs()`` method of
    `scipy.stats.ortho_group`.

    >>> from scipy.stats import ortho_group
    >>> orth = ortho_group.rvs(4)
    >>> svdvals(orth)
    array([ 1.,  1.,  1.,  1.])
    """
    return svd(a, compute_uv=0, overwrite_a=overwrite_a,
               check_finite=check_finite)


def svdvals(x: Array, /, xp: Namespace) -> Array | tuple[Array, ...]:
    return xp.linalg.svd(x, compute_uv=False)


def svdvals(x: Array) -> Array:
    # TODO: can't avoid computing U or V for dask
    _, s, _ =  svd(x)
    return s


def svdvals(x, /):
    """
    Returns the singular values of a matrix (or a stack of matrices) ``x``.
    When x is a stack of matrices, the function will compute the singular
    values for each matrix in the stack.

    This function is Array API compatible.

    Calling ``np.svdvals(x)`` to get singular values is the same as
    ``np.svd(x, compute_uv=False, hermitian=False)``.

    Parameters
    ----------
    x : (..., M, N) array_like
        Input array having shape (..., M, N) and whose last two
        dimensions form matrices on which to perform singular value
        decomposition. Should have a floating-point data type.

    Returns
    -------
    out : ndarray
        An array with shape (..., K) that contains the vector(s)
        of singular values of length K, where K = min(M, N).

    See Also
    --------
    scipy.linalg.svdvals : Compute singular values of a matrix.

    Examples
    --------

    >>> np.linalg.svdvals([[1, 2, 3, 4, 5],
    ...                    [1, 4, 9, 16, 25],
    ...                    [1, 8, 27, 64, 125]])
    array([146.68862757,   5.57510612,   0.60393245])

    Determine the rank of a matrix using singular values:

    >>> s = np.linalg.svdvals([[1, 2, 3],
    ...                        [2, 4, 6],
    ...                        [-1, 1, -1]]); s
    array([8.38434191e+00, 1.64402274e+00, 2.31534378e-16])
    >>> np.count_nonzero(s > 1e-10)  # Matrix of rank 2
    2

    """
    return svd(x, compute_uv=False, hermitian=False)


def svdvals(x: ArrayLike, /) -> Array:
  """Compute the singular values of a matrix.

  JAX implementation of :func:`numpy.linalg.svdvals`.

  Args:
    x: array of shape ``(..., M, N)`` for which singular values will be computed.

  Returns:
    array of singular values of shape ``(..., K)`` with ``K = min(M, N)``.

  See also:
    :func:`jax.numpy.linalg.svd`: compute singular values and singular vectors

  Examples:
    >>> x = jnp.array([[1, 2, 3],
    ...                [4, 5, 6]])
    >>> jnp.linalg.svdvals(x)
    Array([9.508031 , 0.7728694], dtype=float32)
  """
  x = ensure_arraylike('jnp.linalg.svdvals', x)
  return svd(x, compute_uv=False, hermitian=False)

