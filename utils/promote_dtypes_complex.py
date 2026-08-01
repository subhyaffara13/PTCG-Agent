
def promote_dtypes_complex(*args: ArrayLike) -> list[Array]:
  """Convenience function to apply Numpy argument dtype promotion.

  Promotes arguments to a complex type."""
  to_dtype, weak_type = dtypes.lattice_result_type(*args)
  to_dtype_complex = dtypes.to_complex_dtype(to_dtype)
  return [lax._convert_element_type(x, to_dtype_complex, weak_type)
          for x in args]

