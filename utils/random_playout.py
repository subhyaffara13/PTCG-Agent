
def random_playout(state: pyspiel.State, seed: Optional[int] = None):
  """Plays random actions until the state is terminal."""
  rng = np.random.RandomState(seed)
  while not state.is_terminal():
    state.apply_action(rng.choice(state.legal_actions()))
  return state

