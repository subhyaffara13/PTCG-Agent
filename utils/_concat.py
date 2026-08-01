
def _concat(num_microbatches: int) -> Accumulator:
  """An Accumulator that concatenates microbatched outputs along the axis 0."""
  if num_microbatches <= 0:
    raise ValueError(f'{num_microbatches=} must be positive.')

  def init(value):
    shape = (num_microbatches,) + value.shape
    return jnp.broadcast_to(jnp.zeros_like(value), shape)

  def update(carry, value, index):
    return carry.at[index].set(value)

  def finalize(carry):
    kwargs = _get_out_sharding(carry)
    return carry.reshape(-1, *carry.shape[2:], order='F', **kwargs)

  return _lift(Accumulator(init, update, finalize, lambda x: x))


def _concat(a, b): return lax.concatenate([a, b], 0)

