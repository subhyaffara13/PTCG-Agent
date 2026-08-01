
def sequence_weights_to_tabular_profile(root, policy_fn) -> dict:
  """Returns the `dict` of `list`s of action-prob pairs-form of `policy_fn`."""
  tabular_policy = {}
  players = list(range(root.num_players()))
  for state in all_states(root):
    for player in players:
      legal_actions = state.legal_actions(player)
      if len(legal_actions) < 1:
        continue
      info_state = state.information_state_string(player)
      if info_state in tabular_policy:
        continue
      my_policy = policy_fn(state)
      tabular_policy[info_state] = list(zip(legal_actions, my_policy))
  return tabular_policy


def sequence_weights_to_tabular_profile(root, policy_fn) -> dict:
  """Returns the `dict` of `list`s of action-prob pairs-form of `policy_fn`."""
  tabular_policy = {}
  players = list(range(root.num_players()))
  for state in all_states(root):
    for player in players:
      legal_actions = state.legal_actions(player)
      if len(legal_actions) < 1:
        continue
      info_state = state.information_state_string(player)
      if info_state in tabular_policy:
        continue
      my_policy = policy_fn(state)
      tabular_policy[info_state] = list(zip(legal_actions, my_policy))
  return tabular_policy

