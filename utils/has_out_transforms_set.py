
def has_out_transforms_set(op: MlirOperation) -> bool:
  return "out_transforms" in op.attributes

