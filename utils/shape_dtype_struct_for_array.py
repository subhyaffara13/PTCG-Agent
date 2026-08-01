
def shape_dtype_struct_for_array(array: jax.Array) -> jax.ShapeDtypeStruct:
  """Builds a ShapeDtypeStruct from a jax.Array."""
  return cast(
      jax.ShapeDtypeStruct, abstract_arrays.to_shape_dtype_struct(array)
  )

