
def vq(obs, code_book, check_finite=True):
    """
    Assign codes from a code book to observations.

    Assigns a code from a code book to each observation. Each
    observation vector in the 'M' by 'N' `obs` array is compared with the
    centroids in the code book and assigned the code of the closest
    centroid.

    The features in `obs` should have unit variance, which can be
    achieved by passing them through the whiten function. The code
    book can be created with the k-means algorithm or a different
    encoding algorithm.

    Parameters
    ----------
    obs : ndarray
        Each row of the 'M' x 'N' array is an observation. The columns are
        the "features" seen during each observation. The features must be
        whitened first using the whiten function or something equivalent.
    code_book : ndarray
        The code book is usually generated using the k-means algorithm.
        Each row of the array holds a different code, and the columns are
        the features of the code::

            #              f0  f1  f2  f3
            code_book = [[ 1., 2., 3., 4.],  #c0
                         [ 1., 2., 3., 4.],  #c1
                         [ 1., 2., 3., 4.]]  #c2

    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
        Default: True

    Returns
    -------
    code : ndarray
        A length M array holding the code book index for each observation.
    dist : ndarray
        The distortion (distance) between the observation and its nearest
        code.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.cluster.vq import vq
    >>> code_book = np.array([[1., 1., 1.],
    ...                       [2., 2., 2.]])
    >>> features  = np.array([[1.9, 2.3, 1.7],
    ...                       [1.5, 2.5, 2.2],
    ...                       [0.8, 0.6, 1.7]])
    >>> vq(features, code_book)
    (array([1, 1, 0], dtype=int32), array([0.43588989, 0.73484692, 0.83066239]))

    """
    xp = array_namespace(obs, code_book)
    obs = _asarray(obs, xp=xp, check_finite=check_finite)
    code_book = _asarray(code_book, xp=xp, check_finite=check_finite)
    ct = xp.result_type(obs, code_book)

    if xp.isdtype(ct, kind='real floating'):
        c_obs = xp.astype(obs, ct, copy=False)
        c_code_book = xp.astype(code_book, ct, copy=False)
        c_obs = np.asarray(c_obs)
        c_code_book = np.asarray(c_code_book)
        result = _vq.vq(c_obs, c_code_book)
        return xp.asarray(result[0]), xp.asarray(result[1])
    return _py_vq(obs, code_book, check_finite=False)


def vq(obs: ArrayLike, code_book: ArrayLike, check_finite: bool = True) -> tuple[Array, Array]:
  """Assign codes from a code book to a set of observations.

  JAX implementation of :func:`scipy.cluster.vq.vq`.

  Assigns each observation vector in ``obs`` to a code from ``code_book``
  based on the nearest Euclidean distance.

  Args:
    obs: array of observation vectors of shape ``(M, N)``. Each row represents
      a single observation. If ``obs`` is one-dimensional, then each entry is
      treated as a length-1 observation.
    code_book: array of codes with shape ``(K, N)``. Each row represents a single
      code vector. If ``code_book`` is one-dimensional, then each entry is treated
      as a length-1 code.
    check_finite: unused in JAX

  Returns:
    A tuple of arrays ``(code, dist)``

    - ``code`` is an integer array of shape ``(M,)`` containing indices ``0 <= i < K``
      of the closest entry in ``code_book`` for the given entry in ``obs``.
    - ``dist`` is a float array of shape ``(M,)`` containing the euclidean
      distance between each observation and the nearest code.

  Examples:
    >>> obs = jnp.array([[1.1, 2.1, 3.1],
    ...                  [5.9, 4.8, 6.2]])
    >>> code_book = jnp.array([[1., 2., 3.],
    ...                        [2., 3., 4.],
    ...                        [3., 4., 5.],
    ...                        [4., 5., 6.]])
    >>> codes, distances = jax.scipy.cluster.vq.vq(obs, code_book)
    >>> print(codes)
    [0 3]
    >>> print(distances)
    [0.17320499 1.9209373 ]
  """
  del check_finite  # unused
  check_arraylike("scipy.cluster.vq.vq", obs, code_book)
  obs_arr, cb_arr = promote_dtypes_inexact(obs, code_book)
  if obs_arr.ndim != cb_arr.ndim:
      raise ValueError("Observation and code_book should have the same rank")
  if obs_arr.ndim == 1:
      obs_arr, cb_arr = obs_arr[..., None], cb_arr[..., None]
  if obs_arr.ndim != 2:
      raise ValueError("ndim different than 1 or 2 are not supported")
  dist = api.vmap(lambda ob: jnp_linalg.norm(ob[None] - cb_arr, axis=-1))(obs_arr)
  code = jnp.argmin(dist, axis=-1)
  dist_min = api.vmap(operator.getitem)(dist, code)
  return code, dist_min

