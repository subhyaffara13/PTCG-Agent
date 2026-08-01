
def make_dataset(file: str):
  """Creates dataset as a generator of single examples."""
  all_trajectories = [_no_play_trajectory(line) for line in open(file)]
  while True:
    np.random.shuffle(all_trajectories)
    for trajectory in all_trajectories:
      action_index = np.random.randint(52, len(trajectory))
      state = GAME.new_initial_state()
      for action in trajectory[:action_index]:
        state.apply_action(action)
      yield (state.observation_tensor(), trajectory[action_index] - MIN_ACTION)


def make_dataset(file: str):
  """Creates dataset as a generator of single examples."""
  lines = [line for line in open(file)]
  while True:
    np.random.shuffle(lines)
    for line in lines:
      trajectory = _trajectory(line)
      # skip pass_dir and deal actions
      action_index = np.random.randint(NUM_CARDS + 1, len(trajectory))
      state = GAME.new_initial_state()
      for action in trajectory[:action_index]:
        state.apply_action(action)
      yield (state.information_state_tensor(), trajectory[action_index])

