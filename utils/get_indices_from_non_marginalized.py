
def get_indices_from_non_marginalized(policies):
  """Get a list of lists of indices from joint policies.

  These are the ones used for training strategy selector.

  Args:
    policies: a list of joint policies.

  Returns:
    A list of lists of indices.
  """
  num_players = len(policies[0])
  num_strategies = len(policies)
  return [list(range(num_strategies)) for _ in range(num_players)]

