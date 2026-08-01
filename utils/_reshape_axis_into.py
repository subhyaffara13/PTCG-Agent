
def _reshape_axis_into(src, dst, x):
  # NB: `dst` is the number of the dimension that we should reshape into
  # *after* `src` is removed from `x`'s list of dimensions. For example, if
  # `src` is an added batch dimension, `dst` might name a target dimension in
  # the unbatched list of dimensions.
  perm = [i for i in range(x.ndim) if i != src]
  perm.insert(dst, src)
  new_shape = list(np.delete(x.shape, src))
  new_shape[dst] *= x.shape[src]
  return lax.reshape(x, new_shape, perm)

