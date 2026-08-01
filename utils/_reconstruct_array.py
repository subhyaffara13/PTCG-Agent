
def _reconstruct_array(fun, args, arr_state, aval_state):
  """Method to reconstruct a device array from a serialized state."""
  np_value = fun(*args)
  np_value.__setstate__(arr_state)
  jnp_value = api.device_put(np_value)
  jnp_value.aval = jnp_value.aval.update(**aval_state)
  return jnp_value

