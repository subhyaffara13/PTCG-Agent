
def from_heuristic_payoff_table(hpt):
  """Returns a `PayoffTable` instance from a numpy 2D HPT."""
  [num_rows, num_columns] = hpt.shape
  assert num_columns % 2 == 0
  num_strategies = int(num_columns / 2)
  num_players = np.sum(hpt[0, :num_strategies])
  obj = PayoffTable(num_players, num_strategies, initialize_payoff_table=False)

  # pylint: disable=protected-access
  for row in hpt:
    payoff_row = np.array(row[num_strategies:])
    obj._payoff_table[tuple(row[:num_strategies])] = payoff_row

  assert len(obj._payoff_table) == num_rows
  # pylint: enable=protected-access
  return obj

