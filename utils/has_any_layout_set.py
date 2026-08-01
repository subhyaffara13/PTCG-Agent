
def has_any_layout_set(op: MlirOperation) -> bool:
  return has_in_layouts_set(op) or has_out_layouts_set(op)

