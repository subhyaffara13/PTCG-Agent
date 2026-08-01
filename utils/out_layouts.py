
def out_layouts(op: MlirOperation) -> Sequence[ir.Attribute]:
  """Returns the out_layouts attribute of the given operation.

  Raises:
    ValueError: If the operation does not have an out_layouts attribute.
  """
  return _array_attr(op, "out_layouts")

