
def strict_promotion_if_dtypes_match(dtypes):
  """
  Context manager to enable strict promotion if all dtypes match,
  and enable standard dtype promotion otherwise.
  """
  if all(dtype == dtypes[0] for dtype in dtypes):
    return config.numpy_dtype_promotion('strict')
  return config.numpy_dtype_promotion('standard')

