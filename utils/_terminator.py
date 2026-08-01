
def _terminator(
    block: ir.Block, expected_terminator: type[ir.OpView]
) -> ir.OpView:
  """Returns the terminator of the given block.

  Checks that the terminator is of the expected type.
  """
  terminator = block.operations[len(block.operations) - 1]
  assert isinstance(terminator, expected_terminator)
  return terminator.opview

