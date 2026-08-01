
def construct_is_mcts_policy(game, state, tabular_policy, bot, searched):
  """Constructs a tabular policy from independent bot calls.

  Args:
    game: an OpenSpiel game,
    state: an OpenSpiel state to start the tree walk from,
    tabular_policy: a policy.TabularPolicy for this game,
    bot: the bot to get the policy from at each state
    searched: a dictionary of information states already search (empty to begin)
  """

  if state.is_terminal():
    return
  elif state.is_chance_node():
    outcomes = state.legal_actions()
    for outcome in outcomes:
      new_state = state.clone()
      new_state.apply_action(outcome)
      construct_is_mcts_policy(game, new_state, tabular_policy, bot, searched)
  else:
    infostate_key = state.information_state_string()
    if infostate_key not in searched:
      searched[infostate_key] = True
      infostate_policy = bot.get_policy(state)
      tabular_state_policy = tabular_policy.policy_for_key(infostate_key)
      for action, prob in infostate_policy:
        tabular_state_policy[action] = prob
    for action in state.legal_actions():
      new_state = state.clone()
      new_state.apply_action(action)
      construct_is_mcts_policy(game, new_state, tabular_policy, bot, searched)

