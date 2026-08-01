
def _get_regret(agent, state, policy, num_players):
  """Returns the regret for the current state."""
  player = state.current_player()

  mask = state.legal_actions_mask()
  children_values = np.zeros(len(mask), dtype=float)
  for a, m in enumerate(mask):
    if m == 1:
      child = state.child(a)

      with torch.no_grad():
        history = _state_history(num_players, child)
        x = torch.from_numpy(history).to(torch.float32)
        children_values[a] = agent.value_nets[player](x)

  value = np.sum(policy * children_values)
  regret = children_values - value
  return regret

