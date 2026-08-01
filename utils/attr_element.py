
def attr_element(
    attr_name: str, op: MlirOperation, index: int
) -> ir.Attribute | None:
  """Returns `op.attributes[attr_name][index]` if it exists, otherwise None.

  If `op.attributes[attr_name]` exists, then `index` must be a valid index into
  the attribute array.
  """
  if attr_name not in op.attributes:
    return None
  attr = op.attributes[attr_name]
  if not attr:
    return None
  assert isinstance(attr, ir.ArrayAttr)
  return attr[index]

