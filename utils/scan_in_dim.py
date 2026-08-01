
def scan_in_dim(body_fn, init, xs, axis=(0,), unroll=(1,), keepdims=False):
  """utility for doing a scan along arbitrary dimensions.

  See `lax.scan` for details on how the scan operation works.

  Note on `unroll`: This argument gets left padded with ones to match the size
  of `axis`. Doing so allows unrolls to performed from the innermost loop first.
  For example, `scan_in_dim(..., axis=(1, 2, 3), unroll=5)` is equivalent to
  `scan_in_dim(..., axis=(1, 2, 3), unroll=(1, 1, 5))`.

  Args:
    body_fn: the body of the loop of type (c, x) -> (c, y).
    init: initial value for the carry.
    xs: a pytree of tensors to scan over.
    axis: the axis to scan over.
    keepdims: keep the dimensions that are scanned over.
    unroll: an optional positive integer, or tuple of positive integers
      showing how many iterations of the loop to be unrolled into a single
      iteration for each axis.
  Returns:
    A tuple of the final carry and the values returned by the body.
  """
  if not isinstance(axis, Iterable):
    axis = (axis,)

  if not isinstance(unroll, Iterable):
    unroll = (unroll,)

  # Pad unroll with ones so we start unrolling from the innermost loop
  len_diff = len(axis) - len(unroll)
  unroll = (1,) * len_diff + unroll

  def transpose_in(x):
    perm = axis + tuple(np.delete(np.arange(x.ndim), axis))
    return x.transpose(perm)

  def transpose_out(x):
    perm = axis + tuple(np.delete(np.arange(x.ndim), axis))
    return x.transpose(_invert_perm(perm))

  def body_wrapper(c, xs):
    if keepdims:
      xs = jax.tree_util.tree_map(
        lambda x: x.reshape((1,) * len(axis) + x.shape), xs
      )
      xs = jax.tree_util.tree_map(transpose_out, xs)
    c, ys = body_fn(c, xs)
    if keepdims:
      ys = jax.tree_util.tree_map(transpose_in, ys)
      ys = jax.tree_util.tree_map(lambda x: x.reshape(x.shape[len(axis) :]), ys)
    return c, ys

  xs = jax.tree_util.tree_map(transpose_in, xs)
  c, ys = _scan_nd(body_wrapper, init, xs, n=len(axis), unroll=unroll)
  ys = jax.tree_util.tree_map(transpose_out, ys)
  return c, ys

