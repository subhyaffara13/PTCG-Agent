
def represents_jax_array(param_info: types.ParamInfo) -> bool:
  """Returns True if the param_info represents a jax.Array."""
  assert (
      param_info.value_typestr is not None
  ), f'ParamInfo.value_typestr cannot be None: {param_info}'
  return param_info.value_typestr == JAX_ARRAY_TYPE_STR

