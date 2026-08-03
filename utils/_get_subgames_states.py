import itertools

def _get_subgames_states(state, all_states, depth_limit, depth,
                         include_terminals, include_chance_states,
                         include_mean_field_states, to_string,
                         stop_if_encountered):
  """Extract non-chance states for a subgame into the all_states dict."""
  if state.is_terminal():
    if include_terminals:
      # Include if not already present and then terminate recursion.
      state_str = to_string(state)
      if state_str not in all_states:
        all_states[state_str] = state.clone()
    return

  if depth > depth_limit >= 0:
    return
  is_mean_field = state.current_player() == pyspiel.PlayerId.MEAN_FIELD
  if (state.is_chance_node() and
      include_chance_states) or (is_mean_field and
                                 include_mean_field_states) or not (
                                     state.is_chance_node() or is_mean_field):
    # Add only if not already present
    state_str = to_string(state)
    if state_str not in all_states:
      all_states[state_str] = state.clone()
    else:
      # We already saw this one. Stop the recursion if the flag is set
      if stop_if_encountered:
        return

  if is_mean_field:
    support = state.distribution_support()
    state_for_search = state.clone()
    support_length = len(support)
    # update with a dummy distribution
    state_for_search.update_distribution(
        [1.0 / support_length for _ in range(support_length)])
    _get_subgames_states(state_for_search, all_states, depth_limit, depth + 1,
                         include_terminals, include_chance_states,
                         include_mean_field_states, to_string,
                         stop_if_encountered)
  elif state.is_simultaneous_node():
    joint_legal_actions = [
        state.legal_actions(player)
        for player in range(state.get_game().num_players())
    ]
    for joint_actions in itertools.product(*joint_legal_actions):
      state_for_search = state.clone()
      state_for_search.apply_actions(list(joint_actions))
      _get_subgames_states(state_for_search, all_states, depth_limit, depth + 1,
                           include_terminals, include_chance_states,
                           include_mean_field_states, to_string,
                           stop_if_encountered)
  else:
    for action in state.legal_actions():
      state_for_search = state.child(action)
      _get_subgames_states(state_for_search, all_states, depth_limit, depth + 1,
                           include_terminals, include_chance_states,
                           include_mean_field_states, to_string,
                           stop_if_encountered)

