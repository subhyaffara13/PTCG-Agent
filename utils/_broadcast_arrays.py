
def _broadcast_arrays(*arrays):
    """
    Same as np.broadcast_arrays(a, b) but old writeability rules.

    NumPy >= 1.17.0 transitions broadcast_arrays to return
    read-only arrays. Set writeability explicitly to avoid warnings.
    Retain the old writeability rules, as our Cython code assumes
    the old behavior.
    """
    broadcast_arrays = np.broadcast_arrays(*arrays)
    for x, a in zip(broadcast_arrays, arrays):
        x.flags.writeable = a.flags.writeable
    return broadcast_arrays


def _broadcast_arrays(arrays, axis=None, xp=None):
    """
    Broadcast shapes of arrays, ignoring incompatibility of specified axes
    """
    arrays = tuple(arrays)
    if not arrays:
        return arrays
    xp = array_namespace(*arrays) if xp is None else xp
    arrays = [xp.asarray(arr) for arr in arrays]
    shapes = [arr.shape for arr in arrays]
    new_shapes = _broadcast_shapes(shapes, axis)
    if axis is None:
        new_shapes = [new_shapes]*len(arrays)
    return [xp.broadcast_to(array, new_shape)
            for array, new_shape in zip(arrays, new_shapes)]


def _broadcast_arrays(*args: ArrayLike) -> list[Array]:
  """Like Numpy's broadcast_arrays but doesn't return views."""
  avals = [core.shaped_abstractify(arg) for arg in args]
  shapes = [a.shape for a in avals]
  if not shapes or all(core.definitely_equal_shape(shapes[0], s) for s in shapes):
    return [lax.asarray(arg) for arg in args]
  result_shape = lax.broadcast_shapes(*shapes)
  result_sharding = lax.broadcast_shardings(*avals)
  return [_broadcast_to(arg, result_shape, result_sharding) for arg in args]

