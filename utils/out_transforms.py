
def out_transforms(op: MlirOperation) -> Sequence[ir.ArrayAttr]:
  """Returns the out_transforms attribute of the given operation.

  Raises:
    ValueError: If the operation does not have an out_transforms attribute.
  """
  return _array_attr(op, "out_transforms")  # pyrefly: ignore[bad-return]

