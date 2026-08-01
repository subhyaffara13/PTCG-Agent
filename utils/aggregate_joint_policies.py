
def aggregate_joint_policies(game, total_policies,
                             probabilities_of_playing_policies):
  """Aggregate the players' joint policies.

  Specifically, returns a single callable policy object that is
  realization-equivalent to playing total_policies with
  probabilities_of_playing_policies. I.e., aggr_policy is a joint policy that
  can be called at any information state [via
  action_probabilities(state, player_id)].

  Args:
    game: The open_spiel game.
    total_policies: A list of list of all policy.Policy strategies used for
      training, where the n-th entry of the main list is a list of policies, one
      entry for each player.
    probabilities_of_playing_policies: A list of floats representing the
      probabilities of playing each joint strategy in total_policies.

  Returns:
    A callable object representing the policy.
  """
  aggregator = policy_aggregator_joint.JointPolicyAggregator(game)

  return aggregator.aggregate(
      range(len(total_policies[0])), total_policies,
      probabilities_of_playing_policies)

