
def promote_args_complex(fun_name: str, *args: ArrayLike) -> list[Array]:
  """Convenience function to apply Numpy argument shape and dtype promotion.

  Promotes non-complex types to a complex type."""
  check_arraylike(fun_name, *args)
  args = tuple(_check_jax_array_protocol(arg) for arg in args)
  _check_no_float0s(fun_name, *args)
  check_for_prngkeys(fun_name, *args)
  return promote_shapes(fun_name, *promote_dtypes_complex(*args))

