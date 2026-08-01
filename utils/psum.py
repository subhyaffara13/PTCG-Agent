
def psum(x, axis_name, *, axis_index_groups=None):
  """Compute an all-reduce sum on ``x`` over the pmapped axis ``axis_name``.

  If ``x`` is a pytree then the result is equivalent to mapping this function to
  each leaf in the tree.

  Inputs of boolean dtype are converted to integers before the reduction.

  Args:
    x: array(s) with a mapped axis named ``axis_name``.
    axis_name: hashable Python object used to name a pmapped axis (see the
      :func:`jax.pmap` documentation for more details).
    axis_index_groups: optional list of lists containing axis indices (e.g. for
      an axis of size 4, [[0, 1], [2, 3]] would perform psums over the first
      two and last two replicas). Groups must cover all axis indices exactly
      once.

  Returns:
    Array(s) with the same shape as ``x`` representing the result of an
    all-reduce sum along the axis ``axis_name``.

  Examples:
    For example, with 4 XLA devices available:

    >>> x = np.arange(4)
    >>> y = jax.pmap(lambda x: jax.lax.psum(x, 'i'), axis_name='i')(x)
    >>> print(y)
    [6 6 6 6]
    >>> y = jax.pmap(lambda x: x / jax.lax.psum(x, 'i'), axis_name='i')(x)
    >>> print(y)
    [0.         0.16666667 0.33333334 0.5       ]

    Suppose we want to perform ``psum`` among two groups, one with ``device0`` and ``device1``, the other with ``device2`` and ``device3``,

    >>> y = jax.pmap(lambda x: jax.lax.psum(x, 'i', axis_index_groups=[[0, 1], [2, 3]]), axis_name='i')(x)
    >>> print(y)
    [1 1 5 5]

    An example using 2D-shaped x. Each row is data from one device.

    >>> x = np.arange(16).reshape(4, 4)
    >>> print(x)
    [[ 0  1  2  3]
     [ 4  5  6  7]
     [ 8  9 10 11]
     [12 13 14 15]]

    Full ``psum`` across all devices:

    >>> y = jax.pmap(lambda x: jax.lax.psum(x, 'i'), axis_name='i')(x)
    >>> print(y)
    [[24 28 32 36]
     [24 28 32 36]
     [24 28 32 36]
     [24 28 32 36]]

    Perform ``psum`` among two groups:

    >>> y = jax.pmap(lambda x: jax.lax.psum(x, 'i', axis_index_groups=[[0, 1], [2, 3]]), axis_name='i')(x)
    >>> print(y)
    [[ 4  6  8 10]
     [ 4  6  8 10]
     [20 22 24 26]
     [20 22 24 26]]
  """
  return _psum_is_async(x, axis_name, axis_index_groups=axis_index_groups,
                        is_async=False)

