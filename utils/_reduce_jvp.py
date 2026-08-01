
def _reduce_jvp(reducer, init_values, primals, tangents, axes):
  input_shape = np.array(primals[0].shape, dtype=int)

  n = np.prod(input_shape[list(axes)])
  non_axes = np.delete(np.arange(len(input_shape)), axes)

  # Move the reduced axes to the front, and flatten them to 1D.
  permutation = axes + tuple(non_axes)
  new_shape = (n,) + tuple(input_shape[non_axes])
  primals = tuple(reshape(x, new_shape, permutation) for x in primals)
  tangents = tuple(reshape(t, new_shape, permutation) for t in tangents)

  for d in range(len(non_axes) + 1):
    reducer = api.vmap(reducer)
  def _reduce_tree(*xs, axis=0):
    """Reduce by repeatedly splitting the array and multiplying."""
    while xs[0].shape[axis] > 1:
      n = xs[0].shape[axis]
      n1 = (n + 1) // 2
      n2 = n - n1
      xs1 = [slicing.slice_in_dim(x, 0, n1) for x in xs]
      xs2 = [slicing.slice_in_dim(x, n1, None) for x in xs]
      if n2 != n1:
        paddings = [(0, 0, 0)] * len(xs[0].shape)
        paddings[axis] = (0, 1, 0)
        xs2 = [pad(x2, i, paddings) for x2, i in zip(xs2, init_values)]
      xs = reducer(*(xs1 + xs2))
    if xs[0].shape[axis] == 0:
      return [full(tuple(input_shape[non_axes]), i) for i in init_values]
    return tuple(squeeze(x, (axis,)) for x in xs)

  return api.jvp(_reduce_tree, primals, tangents)

