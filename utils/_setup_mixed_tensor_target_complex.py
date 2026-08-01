
def _setup_mixed_tensor_target_complex(dtype):
  """Complex version of _common_test._setup_mixed_tensor_target."""
  initial_params = jnp.zeros((2, 2), dtype=dtype)
  final_params = jnp.array(
      [[1.0 + 2.0j, 0.0], [-1.0 + 1.0j, 1.0 - 3.0j]],
      dtype=dtype,
  )

  def obj_fn(params):
    return jnp.sum(numerics.abs_sq(params - final_params))

  return initial_params, final_params, obj_fn

