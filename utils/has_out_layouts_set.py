
def has_out_layouts_set(op: MlirOperation) -> bool:
  return "out_layouts" in op.attributes

