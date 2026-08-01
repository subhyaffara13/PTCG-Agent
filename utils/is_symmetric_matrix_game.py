
def is_symmetric_matrix_game(payoff_tables):
  """Checks if payoff_tables corresponds to a symmetric matrix game."""
  payoffs_are_hpt_format = check_payoffs_are_hpt(payoff_tables)

  if len(payoff_tables) == 2:
    if payoffs_are_hpt_format and np.array_equal(payoff_tables[0](),
                                                 payoff_tables[1]()):
      return True, [payoff_tables[0]]
    elif ~payoffs_are_hpt_format and np.array_equal(payoff_tables[0],
                                                    payoff_tables[1].T):
      return True, [payoff_tables[0]]
  return False, payoff_tables

