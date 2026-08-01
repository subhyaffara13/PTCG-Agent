
def _reconstruct_dist(eliminated_dist, action_labels, num_actions):
  """Returns reconstructed dist from eliminated_dist and action_labels.

  Redundant dist elements are given values 0.

  Args:
    eliminated_dist: Array of shape [A0E, A1E, ...].
    action_labels: List of length N and shapes [[A0E], [A1E], ...].
    num_actions: List of length N and values [A0, A1, ...].

  Returns:
    reconstructed_dist: Array of shape [A0, A1, ...].
  """
  reconstructed_payoff = np.zeros(num_actions)
  reconstructed_payoff[np.ix_(*action_labels)] = eliminated_dist
  return reconstructed_payoff

