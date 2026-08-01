
def psum_scatter(x, axis_name, *, scatter_dimension=0, axis_index_groups=None,
                 tiled=False):
  """
  Like ``psum(x, axis_name)`` but each device retains only part of the result.

  For example, ``psum_scatter(x, axis_name, scatter_dimension=0, tiled=False)``
  computes the same value as ``psum(x, axis_name)[axis_index(axis_name)]``, but
  it is more efficient. Thus the ``psum`` result is left scattered along the
  mapped axis.

  One efficient algorithm for computing ``psum(x, axis_name)`` is to perform a
  ``psum_scatter`` followed by an ``all_gather``, essentially evaluating
  ``all_gather(psum_scatter(x, axis_name))``. So we can think of
  ``psum_scatter`` as "the first half" of a ``psum``.

  Args:
    x: array(s) with a mapped axis named ``axis_name``.
    axis_name: hashable Python object used to name a mapped axis (see the
      :func:`jax.pmap` documentation for more details).
    scatter_dimension: a positional axis into which the all-reduce result along
      ``axis_name`` will be scattered.
    axis_index_groups: optional list of lists of integers containing axis
      indices. For example, for an axis of size 4,
      ``axis_index_groups=[[0, 1], [2, 3]]`` would run reduce-scatter over the
      first two and the last two axis indices. Groups must cover all axis
      indices exactly once, and all groups must be the same size.
    tiled: boolean representing whether to use rank-preserving 'tiled' behavior.
      When ``False`` (the default value), the size of dimension in
      ``scatter_dimension`` must match the size of axis ``axis_name`` (or the
      group size if ``axis_index_groups`` is given). After scattering the
      all-reduce result along ``scatter_dimension``, the output is squeezed by
      removing ``scatter_dimension``, so the result has lower rank than the
      input. When ``True``, the size of dimension in ``scatter_dimension`` must
      be divisible by the size of axis ``axis_name`` (or the group size if
      ``axis_index_groups`` is given), and the ``scatter_dimension`` axis is
      preserved (so the result has the same rank as the input).

  Returns:
    Array(s) with the similar shape as ``x``, except the size of dimension in
    position ``scatter_dimension`` is divided by the size of axis ``axis_name``
    (when ``tiled=True``), or the dimension in position ``scatter_dimension`` is
    eliminated (when ``tiled=False``).

  For example, with 4 XLA devices available:

  >>> x = np.arange(16).reshape(4, 4)
  >>> print(x)
  [[ 0  1  2  3]
   [ 4  5  6  7]
   [ 8  9 10 11]
   [12 13 14 15]]
  >>> y = jax.pmap(lambda x: jax.lax.psum_scatter(x, 'i'), axis_name='i')(x)
  >>> print(y)
  [24 28 32 36]

  if using tiled:

  >>> y = jax.pmap(lambda x: jax.lax.psum_scatter(x, 'i', tiled=True), axis_name='i')(x)
  >>> print(y)
  [[24]
   [28]
   [32]
   [36]]

  An example of using axis_index_groups:

  >>> def f(x):
  ...   return jax.lax.psum_scatter(
  ...       x, 'i', axis_index_groups=[[0, 2], [3, 1]], tiled=True)
  >>> y = jax.pmap(f, axis_name='i')(x)
  >>> print(y)
  [[ 8 10]
   [20 22]
   [12 14]
   [16 18]]
  """
  return _psum_scatter_is_async(x, axis_name,
                                scatter_dimension=scatter_dimension,
                                axis_index_groups=axis_index_groups,
                                tiled=tiled, is_async=False)

