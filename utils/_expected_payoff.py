
def _expected_payoff(row_probabilities, payoffs, strategy, num_players):
  # pylint: disable=g-doc-args
  r"""Returns the expected payoff.

  Computes (with p=num_players):

  r_j = \sum_i row_probabilities[i] * payoffs[i, j] / (1 - (1-strategy[j])^p)
  """
  # pylint: enable=g-doc-args
  [num_rows] = row_probabilities.shape
  [num_rows_2, num_strategies] = payoffs.shape
  [num_strategies_2] = strategy.shape
  assert num_rows == num_rows_2
  assert num_strategies == num_strategies_2

  # One per pure strategy.
  numerators = np.dot(np.transpose(payoffs), row_probabilities)
  # One per pure strategy.
  denominators = 1 - np.power(1 - strategy, num_players)
  return numerators / denominators

