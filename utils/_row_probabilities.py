
def _row_probabilities(coefficients, distributions, strategy):
  """Returns the row probabilities [num_rows].

  Args:
    coefficients: The multinomial coefficients [num_rows].
    distributions: The distributions table [num_rows, num_strategies].
    strategy: The strategy array [num_strategies].
  """
  row_probabilities = coefficients * np.prod(
      np.power(strategy, distributions), axis=1)
  return row_probabilities

