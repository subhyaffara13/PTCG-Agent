
def build_lapack_fn_target(fn_base: str, dtype) -> str:
  """Builds the target name for a LAPACK function custom call."""
  try:
    prefix = (
        LAPACK_DTYPE_PREFIX.get(dtype, None) or LAPACK_DTYPE_PREFIX[dtype.type]
    )
    return f"lapack_{prefix}{fn_base}"
  except KeyError as err:
    raise NotImplementedError(err, f"Unsupported dtype {dtype}.") from err

