
def angle_between(
    x0: FloatArray[..., 3],
    x1: FloatArray[..., 3],
    *,
    keepdims: bool = False,
    xnp: numpy_utils.NpModule = ...,
) -> FloatArray['... 1?']:
  """Compute angle between 2 vectors, unsigned."""
  a0 = compat.norm(xnp.cross(x0, x1), axis=-1, keepdims=keepdims)
  a1 = batch_dot(x0, x1, keepdims=keepdims)
  angle = xnp.arctan2(a0, a1)
  return angle

