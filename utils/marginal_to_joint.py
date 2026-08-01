
def marginal_to_joint(policies):
  """Marginal policies to joint policies.

  Args:
    policies: List of list of policies, one list per player.

  Returns:
    Joint policies in the right order (np.reshape compatible).
  """
  shape = tuple([len(a) for a in policies])
  num_players = len(shape)
  total_length = np.prod(shape)
  indexes = np.array(list(range(total_length)))
  joint_indexes = np.unravel_index(indexes, shape)

  joint_policies = []
  for joint_index in zip(*joint_indexes):
    joint_policies.append([
        policies[player][joint_index[player]] for player in range(num_players)
    ])
  return joint_policies

