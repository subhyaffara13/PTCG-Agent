
def tabular_policy_from_callable(game, callable_policy, players=None):
  """Converts a legacy callable policy into a TabularPolicy.

  Recommendation - instead of using this to convert your policy for evaluation
  purposes, work directly with a `TabularPolicy` if possible.
  Second choice - work with a `Policy` class and call `to_tabular` as needed.

  Args:
    game: The game for which we want a TabularPolicy.
    callable_policy: A callable: state -> action probabilities dict or list.
    players: List of players this policy applies to. If `None`, applies to all
      players.

  Returns:
    A TabularPolicy that materializes the callable policy.
  """
  tabular_policy = TabularPolicy(game, players)
  for state_index, state in enumerate(tabular_policy.states):
    action_probabilities = dict(callable_policy(state))
    infostate_policy = [
        action_probabilities.get(action, 0.)
        for action in range(game.num_distinct_actions())
    ]
    tabular_policy.action_probability_array[state_index, :] = infostate_policy
  return tabular_policy

