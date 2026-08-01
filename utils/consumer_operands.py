
def consumer_operands(result: ValueSite) -> Sequence[ValueSite]:
  """Given a result or an argument, returns the corresponding operands in its consumers."""
  assert result.type in (VariableType.RESULT, VariableType.ARGUMENT)
  results: list[ValueSite] = []
  # The layout can also be chosen from the layout of the consumers of the
  # results.
  for use in result.value.uses:
    consumer = use.owner
    index = use.operand_number
    results.append(ValueSite(consumer, VariableType.OPERAND, index))
  return results

