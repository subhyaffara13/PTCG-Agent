
def project_onto_vector(
    u: FloatArray[..., 3],
    v: FloatArray[..., 3],
) -> FloatArray[..., 3]:
  """Project `u` onto `v`."""
  return (
      batch_dot(u, v, keepdims=True)
      / compat.norm(v, axis=-1, keepdims=True) ** 2
      * v
  )

