
def random_policy(rnd, state):
  # all actions are legal for now
  rnd_action = tuple([rnd.choice(a) for a in state.num_actions])
  return np.ravel_multi_index(rnd_action, state.num_actions)

