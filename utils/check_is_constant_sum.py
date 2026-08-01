
def check_is_constant_sum(payoff_table, payoffs_are_hpt_format):
  """Checks if single-population matrix game is constant-sum.

  Args:
    payoff_table: Either a 2D numpy array, or a _PayoffTableInterface object.
    payoffs_are_hpt_format: Boolean indicating whether payoff table is a
      _PayoffTableInterface object (AKA Heuristic Payoff Table or HPT), or a 2D
      numpy array. True indicates HPT, and False indicates numpy array.

  Returns:
    is_constant_sum: Boolean, True if constant-sum game.
    payoff_sum: Payoff sum if game is constant-sum, or None if not.
  """

  if payoffs_are_hpt_format:
    payoff_sum_table = np.asarray(payoff_table._payoffs).sum(axis=1)  # pylint: disable=protected-access
    is_constant_sum = np.isclose(
        payoff_sum_table, payoff_sum_table[0], atol=1e-14).all()
    payoff_sum = payoff_sum_table[0] if is_constant_sum else None
  else:
    payoff_sum_table = payoff_table + payoff_table.T
    is_constant_sum = np.isclose(
        payoff_sum_table, payoff_sum_table[0, 0], atol=1e-14).all()
    payoff_sum = payoff_sum_table[0, 0] if is_constant_sum else None
  return is_constant_sum, payoff_sum

