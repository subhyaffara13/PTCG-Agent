
def batch_dot(
    x0: FloatArray['... n'],
    x1: FloatArray['... n'],
    *,
    keepdims: bool = False,
    xnp: numpy_utils.NpModule = ...,
) -> FloatArray['... 1?']:
  """Dot product on the last dimension, with broadcasting support.

  Contrary to `np.dot`, the behavior is consistent for 1-dim vs n-dim (while
  dot act as matmul).
  First dimensions are always broadcasted.

  Args:
    x0: Vector array
    x1: Vector array
    keepdims: If True, returns `FloatArray['... 1']`
    xnp: Numpy module to use

  Returns:
    The dot product along the last axis.
  """
  # Weirdly, this doesn't seem np has a native ops for this:
  # * `np.dot`: 1-D vs 2-D behave differently
  # * `np.matmul`: Different op (`kj,jn` vs `...k,...k`)
  # * `np.tensordot`: Weird broadcasting
  # * `np.inner`: Weird broadcasting
  y = xnp.einsum('...m,...m->...', x0, x1)
  return y[..., None] if keepdims else y

