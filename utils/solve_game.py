
def solve_game(state):
  state_str = str(state)
  if state_str in solved:
    return solved[state_str].value
  if state.is_terminal():
    return state.returns()[0]

  max_player = state.current_player() == 0
  obs = state.observation_tensor()
  act_mask = np.array(state.legal_actions_mask())
  values = np.full(act_mask.shape, -2 if max_player else 2)
  for action in state.legal_actions():
    values[action] = solve_game(state.child(action))
  value = values.max() if max_player else values.min()
  best_actions = np.where((values == value) & act_mask)
  policy = np.zeros_like(act_mask)
  policy[best_actions[0][0]] = 1  # Choose the first for a deterministic policy.
  solved[state_str] = utils.TrainInput(
      observation=jnp.asarray(obs, dtype=jnp.float32),
      legals_mask=jnp.asarray(act_mask, dtype=jnp.bool),
      policy=jnp.asarray(policy, dtype=jnp.float32),
      value=jnp.asarray(value, dtype=jnp.float32),
  )
  return value

