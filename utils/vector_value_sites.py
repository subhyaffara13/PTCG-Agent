
def vector_value_sites(op: ir.OpView) -> list[ValueSite]:
  """Returns all the vector operands and results for the given op."""
  value_sites = [
      ValueSite(op, VariableType.OPERAND, i)
      for i, o in enumerate(op.operands)
      if is_vector(o)
  ]
  value_sites.extend([
      ValueSite(op, VariableType.RESULT, i)
      for i, o in enumerate(op.results)
      if is_vector(o)
  ])
  return value_sites

