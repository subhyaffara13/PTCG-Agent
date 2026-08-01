
def has_in_layouts_set(op: MlirOperation) -> bool:
  return "in_layouts" in op.attributes

