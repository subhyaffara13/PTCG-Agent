
def best_response(game, policy, player_id):
  """Returns information about the specified player's best response.

  Given a game and a policy for every player, computes for a single player their
  best unilateral strategy. Returns the value improvement that player would
  get, the action they should take in each information state, and the value
  of each state when following their unilateral policy.

  Args:
    game: An open_spiel game, e.g. kuhn_poker
    policy: A `policy.Policy` object. This policy should depend only on the
      information state available to the current player, but this is not
      enforced.
    player_id: The integer id of a player in the game for whom the best response
      will be computed.

  Returns:
    A dictionary of values, with keys:
      best_response_action: The best unilateral strategy for `player_id` as a
        map from infostatekey to action_id.
      best_response_state_value: The value obtained for `player_id` when
        unilaterally switching strategy, for each state.
      best_response_value: The value obtained for `player_id` when unilaterally
        switching strategy.
      info_sets: A dict of info sets, mapping info state key to a list of
        `(state, counterfactual_reach_prob)` pairs.
      nash_conv: `best_response_value - on_policy_value`
      on_policy_value: The value for `player_id` when all players follow the
        policy
      on_policy_values: The value for each player when all players follow the
        policy
  """
  root_state = game.new_initial_state()
  br = pyspiel_best_response.BestResponsePolicy(game, player_id, policy,
                                                root_state)
  on_policy_values = _state_values(root_state, game.num_players(), policy)
  best_response_value = br.value(root_state)

  # Get best response action for unvisited states
  for infostate in set(br.infosets) - set(br.cache_best_response_action):
    br.best_response_action(infostate)

  return {
      "best_response_action": br.cache_best_response_action,
      "best_response_state_value": br.cache_value,
      "best_response_value": best_response_value,
      "info_sets": br.infosets,
      "nash_conv": best_response_value - on_policy_values[player_id],
      "on_policy_value": on_policy_values[player_id],
      "on_policy_values": on_policy_values,
  }

