
def _state_history(num_players, state):
  history = []
  for p in range(num_players):
    history += state.information_state_tensor(p)
  return np.array(history, dtype=float)

