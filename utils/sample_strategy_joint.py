
def sample_strategy_joint(total_policies, probabilities_of_playing_policies):
  """Samples strategies given joint probabilities.

  Uses independent sampling if probs_are_marginal, and joint sampling otherwise.

  Args:
    total_policies: A list, each element a list of each player's policies.
    probabilities_of_playing_policies: This is a list of play probabilities of
      the joint policies specified by total_policies.

  Returns:
    sampled_policies: A list specifying a single sampled joint strategy.
  """

  sampled_index = sample_random_tensor_index(probabilities_of_playing_policies)
  sampled_policies = []
  for player in range(len(sampled_index)):
    ind = sampled_index[player]
    sampled_policies.append(total_policies[player][ind])
  return sampled_policies

