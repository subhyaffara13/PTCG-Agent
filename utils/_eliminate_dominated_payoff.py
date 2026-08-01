
def _eliminate_dominated_payoff(
    payoff, epsilon, action_labels=None, action_repeats=None, weakly=False):
  """Eliminate epsilon dominated strategies."""
  num_players = payoff.shape[0]
  eliminated = True
  if action_labels is None:
    action_labels = [np.arange(na, dtype=np.int32) for na in payoff.shape[1:]]
  if action_repeats is not None:
    action_repeats = [ar for ar in action_repeats]
  while eliminated:
    eliminated = False
    for p in range(num_players):
      if epsilon > 0.0:
        continue
      num_actions = payoff.shape[1:]
      if num_actions[p] <= 1:
        continue
      for a in range(num_actions[p]):
        index = [slice(None) for _ in range(num_players)]
        index[p] = slice(a, a+1)
        if weakly:
          diff = payoff[p] <= payoff[p][tuple(index)]
        else:
          diff = payoff[p] < payoff[p][tuple(index)]
        axis = tuple(range(p)) + tuple(range(p+1, num_players))
        less = np.all(diff, axis=axis)
        less[a] = False  # Action cannot eliminate itself.
        if np.any(less):
          nonzero = np.nonzero(less)
          payoff = np.delete(payoff, nonzero, axis=p+1)
          action_labels[p] = np.delete(action_labels[p], nonzero)
          if action_repeats is not None:
            action_repeats[p] = np.delete(action_repeats[p], nonzero)
          eliminated = True
          break
  return payoff, action_labels, action_repeats

