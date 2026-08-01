
def in_transforms(op: MlirOperation) -> Sequence[ir.ArrayAttr]:
  """Returns the in_transforms attribute of the given operation.

  Raises:
    ValueError: If the operation does not have an in_transforms attribute.
  """
  return _array_attr(op, "in_transforms")  # pyrefly: ignore[bad-return]

