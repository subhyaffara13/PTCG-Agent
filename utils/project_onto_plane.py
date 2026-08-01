
def project_onto_plane(
    u: FloatArray[..., 3],
    n: FloatArray[..., 3],
) -> FloatArray[..., 3]:
  """Project `u` onto the plane `n` (orthogonal vector)."""
  return u - project_onto_vector(u, n)

