
def _vector_value_sites_and_assignments_for_async_ops(
    op: mgpu.AsyncLoadOp | mgpu.AsyncStoreOp | mgpu.AsyncPrefetchOp,
) -> tuple[ValueSitesForVariable, dict[cs.Variable, cs.Constant]]:
  values_sites: ValueSitesForVariable = dict()
  assignments: dict[cs.Variable, cs.Constant] = dict()

  match op:
    case mgpu.AsyncLoadOp():
      base_operand_index = 3
    case mgpu.AsyncStoreOp():
      base_operand_index = 2
    case mgpu.AsyncPrefetchOp():
      base_operand_index = 1

  for i, idx in enumerate(op.indices):
    if isinstance(idx.type, ir.VectorType):
      value_site = ValueSite(op, VariableType.OPERAND, base_operand_index + i)
      value_site_var = cs.Variable(value_site)
      shape = tuple(idx.type.shape)

      # TODO(cperivol): Move this choice of layouts to the conjuring
      # logic so we can backtrack in case of incompatibility with user
      # annotations.
      if shape[0] % 16 == 0:
        layout = cs.RegisterLayout(value=fa.TMA_INDICES_LAYOUT)
      elif shape[0] % 4 == 0:
        layout = cs.RegisterLayout(value=fa.TMA_INDICES_4_LAYOUT)
      else:
        raise ValueError(f"Unsupported TMA index shape {shape}")
      values_sites[value_site_var] = [value_site]
      assignments[value_site_var] = layout
  return values_sites, assignments

