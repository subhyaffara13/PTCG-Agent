
def _eliminate_dominated_decorator(func):
  """Wrap eliminate dominated."""
  def wrapper(payoff, per_player_repeats, *args, eliminate_dominated=True,
              **kwargs):
    epsilon = getattr(kwargs, "epsilon", 0.0)
    if not eliminate_dominated:
      return func(payoff, *args, **kwargs)
    num_actions = payoff.shape[1:]
    (eliminated_payoff, action_labels, eliminated_action_repeats) = (
        _eliminate_dominated_payoff(
            payoff, epsilon, action_repeats=per_player_repeats
        )
    )
    eliminated_dist, meta = func(
        eliminated_payoff, eliminated_action_repeats, *args, **kwargs)
    meta["eliminated_dominated_dist"] = eliminated_dist
    meta["eliminated_dominated_payoff"] = eliminated_payoff
    dist = _reconstruct_dist(
        eliminated_dist, action_labels, num_actions)
    return dist, meta
  return wrapper

