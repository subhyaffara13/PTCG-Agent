
def valid_jaxtype(x) -> bool:
  try:
    aval = typeof(x)
  except TypeError:
    return False
  else:
    if hasattr(aval, "dtype") and aval.dtype == dtypes.string_dtype:
      return False
    else:
      return True

