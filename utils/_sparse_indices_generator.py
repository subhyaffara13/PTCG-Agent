
def _sparse_indices_generator(player, action, num_actions):
  indices = [(action,) if p == player else range(na)
             for p, na in enumerate(num_actions)]
  return itertools.product(*indices)

