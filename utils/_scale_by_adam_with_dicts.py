
def _scale_by_adam_with_dicts():
  """An implementation of adam using dictionary-based opt states."""

  t = transform.scale_by_adam()

  def init(params):
    state = t.init(params)
    state = cast(transform.ScaleByAdamState, state)

    return ScaleByAdamStateDict(
        count=state.count,
        params={'mu': state.mu, 'nu': state.nu},
    )

  def update(updates, state, params=None):
    state = transform.ScaleByAdamState(
        count=state['count'],
        mu=state['params']['mu'],
        nu=state['params']['nu'],
    )

    _, state = t.update(updates, state, params)
    state = cast(transform.ScaleByAdamState, state)
    return ScaleByAdamStateDict(
        count=state.count,
        params={'mu': state.mu, 'nu': state.nu},
    )

  return base.GradientTransformation(init, update)

