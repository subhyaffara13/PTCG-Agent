
def _default_is_signed(dtype: ir.Type) -> bool | None:
  """Returns `False` for Integer types, `None` otherwise.

  When converting from Pallas dtype to IR type, we lose the `is_signed`
  information. We can default to `False` for most use cases.
  """
  return False if isinstance(dtype, ir.IntegerType) else None

