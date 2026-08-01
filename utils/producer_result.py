
def producer_result(operand: ValueSite) -> ValueSite:
  """Given an operand, returns the corresponding result in its producer.

  When the producer is a block, we return the corresponding operand in the
  operation that owns the block.
  """
  assert operand.type == VariableType.OPERAND
  value = operand.value
  producer = value.owner
  if isinstance(producer, ir.OpView):
    index = list[ir.Value](producer.results).index(value)
    return ValueSite(producer, VariableType.RESULT, index)

  if isinstance(producer, ir.Block):
    index = list[ir.Value](producer.arguments).index(value)
    region_index = list(producer.owner.regions).index(producer.region)
    return ValueSite(producer.owner, VariableType.ARGUMENT, index, region_index)

  raise TypeError(
      f"Producer {producer} is not an operation nor a block: {type(producer)}."
  )

