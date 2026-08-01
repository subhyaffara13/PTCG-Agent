
def _setup_matrix_parabola(dtype):
  """Quadratic function as an optimization target with 2D tensor parameters."""
  initial_params = jnp.zeros((2, 2), dtype=dtype)
  final_params = jnp.array([[3.0, -2.0], [1.0, 4.0]], dtype=dtype)

  def obj_fn(params):
    return jnp.sum(numerics.abs_sq(params - final_params))

  return initial_params, final_params, obj_fn

