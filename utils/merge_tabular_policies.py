
def merge_tabular_policies(tabular_policies, game):
  """Merges n_player policies into single joint policy.

  Missing states are filled with a valid uniform policy.

  Args:
    tabular_policies: List of python TabularPolicy (one for each player).
    game: The game corresponding to the resulting TabularPolicy.

  Returns:
    merged_policy: A TabularPolicy with each player i's policy taken from the
      ith joint_policy.
  """
  if len(tabular_policies) != game.num_players():
    raise ValueError("len(tabular_policies) != num_players: %d != %d" %
                     (len(tabular_policies), game.num_players()))
  merged_policy = TabularPolicy(game)
  for p, p_states in enumerate(merged_policy.states_per_player):
    for p_state in p_states:
      to_index = merged_policy.state_lookup[p_state]
      # Only copy if the state exists, otherwise fall back onto uniform.
      if p_state in tabular_policies[p].state_lookup:
        from_index = tabular_policies[p].state_lookup[p_state]
        merged_policy.action_probability_array[to_index] = (
            tabular_policies[p].action_probability_array[from_index])
  return merged_policy

