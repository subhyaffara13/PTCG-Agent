
def _in_attr_for_operand(
    op: MlirOperation,
    operand: ir.Value,
    attr_name: str,
) -> ir.Attribute | None:
  if attr_name == "in_layouts":
    predicate = lambda v: isinstance(v.type, ir.VectorType)
  elif attr_name == "in_transforms":
    predicate = is_transformable_smem_memref
  elif attr_name == "in_tmem_layouts":
    predicate = (
        lambda v: isinstance(v.type, ir.MemRefType)
        and ir.MemRefType(v.type).memory_space == utils.tmem()
    )
  else:
    raise ValueError(f"Unknown attribute: {attr_name}")

  operand_number = [o for o in op.operands if predicate(o)].index(operand)

  return attr_element(attr_name, op, operand_number)

