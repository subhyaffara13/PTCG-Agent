
def promote_dtypes_numeric(*args: ArrayLike) -> list[Array]:
  """Convenience function to apply Numpy argument dtype promotion.

  Promotes arguments to a numeric (non-bool) type."""
  to_dtype, weak_type = dtypes.lattice_result_type(*args)
  to_dtype_numeric = dtypes.to_numeric_dtype(to_dtype)
  return [lax._convert_element_type(x, to_dtype_numeric, weak_type)
          for x in args]

