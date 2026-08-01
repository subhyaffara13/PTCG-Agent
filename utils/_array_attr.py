
def _arrayAttr(x, context):
    return ArrayAttr.get(x, context=context)


def _array_attr(op: MlirOperation, name: str) -> Sequence[ir.Attribute]:
  try:
    result = op.attributes[name]
  except KeyError:
    raise ValueError(f"{op} does not have an {name} attribute") from None
  if not isinstance(result, ir.ArrayAttr):
    raise TypeError(f"{op} has {name} of an unexpected type: {result}")
  return result  # pyrefly: ignore[bad-return]

