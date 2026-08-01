
def in_layouts(op: MlirOperation) -> Sequence[ir.Attribute]:
  """Returns the in_layouts attribute of the given operation.

  Raises:
    ValueError: If the operation does not have an in_layouts attribute.
  """
  return _array_attr(op, "in_layouts")

