
def _setup_mixed_tensor_target(dtype):
  """Optimization target combining 1D and 2D tensor parameters."""
  initial_1d_params = jnp.zeros((3,), dtype=dtype)
  final_1d_params = jnp.array([1.0, -1.0, 2.0], dtype=dtype)

  initial_2d_params = jnp.zeros((2, 2), dtype=dtype)
  final_2d_params = jnp.array([[1.0, 0.0], [-1.0, 1.0]], dtype=dtype)

  def obj_fn(params):
    """Objective function combining 1D and 2D parameters."""
    params_1d, params_2d = params
    loss_1d = jnp.sum(numerics.abs_sq(params_1d - final_1d_params))
    loss_2d = jnp.sum(numerics.abs_sq(params_2d - final_2d_params))
    return loss_1d + loss_2d

  initial_params = (initial_1d_params, initial_2d_params)
  final_params = (final_1d_params, final_2d_params)

  return initial_params, final_params, obj_fn

