
def is_fake_array(array: Array) -> bool:
  """Returns `True` if the given array is a fake array."""
  return (
      (lazy.has_jax and isinstance(array, lazy.jax.ShapeDtypeStruct))
      or (lazy.has_tf and isinstance(array, lazy.tf.TensorSpec))
      or isinstance(array, ArraySpec)
      or _is_orbax(array)
      or _is_grain(array)
      or _is_pygrain(array)
      or _is_flax_summary(array)
      or isinstance(array, array_types.ArrayAliasMeta)
  )

