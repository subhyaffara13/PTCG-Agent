
def _running_mean() -> Accumulator:
  """An Accumulator that computes the running mean of microbatched outputs."""
  def update(carry, value, index):
    p = index / (index + 1)
    new_state = carry * p + value * (1 - p)
    return new_state

  return _lift(
      Accumulator(
          init=_with_floating_check(jnp.zeros_like),
          update=update,
          finalize=lambda x: x,
          aggregate=functools.partial(jnp.mean, axis=0),
      )
  )

