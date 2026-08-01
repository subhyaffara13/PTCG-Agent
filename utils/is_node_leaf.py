
def is_node_leaf(x: tp.Any) -> tpe.TypeGuard[LeafType]:
  return isinstance(x, LeafType) or variablelib.is_array_ref(x)  # type: ignore[misc, arg-type]

