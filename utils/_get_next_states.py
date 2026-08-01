
def _get_next_states(state, next_states, to_string):
  """Extract non-chance states for a subgame into the all_states dict."""
  is_mean_field = state.current_player() == pyspiel.PlayerId.MEAN_FIELD
  if state.is_chance_node():
    # Add only if not already present

    for action, _ in state.chance_outcomes():
      next_state = state.child(action)
      state_str = to_string(next_state)
      if state_str not in next_states:
        next_states[state_str] = next_state

  if is_mean_field:
    support = state.distribution_support()
    next_state = state.clone()
    support_length = len(support)
    # update with a dummy distribution
    next_state.update_distribution(
        [1.0 / support_length for _ in range(support_length)])
    state_str = to_string(next_state)
    if state_str not in next_states:
      next_states[state_str] = next_state

  if int(state.current_player()) >= 0:
    for action in state.legal_actions():
      next_state = state.child(action)
      state_str = to_string(next_state)
      if state_str not in next_states:
        next_states[state_str] = next_state

