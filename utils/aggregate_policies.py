
def aggregate_policies(game, total_policies, probabilities_of_playing_policies):
  """Aggregate the players' policies.

  Specifically, returns a single callable policy object that is
  realization-equivalent to playing total_policies with
  probabilities_of_playing_policies. I.e., aggr_policy is a joint policy that
  can be called at any information state [via
  action_probabilities(state, player_id)].

  Args:
    game: The open_spiel game.
    total_policies: A list of list of all policy.Policy strategies used for
      training, where the n-th entry of the main list is a list of policies
      available to the n-th player.
    probabilities_of_playing_policies: A list of arrays representing, per
      player, the probabilities of playing each policy in total_policies for the
      same player.

  Returns:
    A callable object representing the policy.
  """
  aggregator = policy_aggregator.PolicyAggregator(game)

  return aggregator.aggregate(
      range(len(probabilities_of_playing_policies)), total_policies,
      probabilities_of_playing_policies)

