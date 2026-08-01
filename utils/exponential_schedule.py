
def exponential_schedule(
    start_e: float, end_e: float, duration: float
) -> Callable[[int], float]:
  @jax.jit
  def _call(t: int) -> float:
    return end_e + (start_e - end_e) * jnp.exp(-1.0 * t / duration)

  return _call


def exponential_schedule(
    start_e: float, end_e: float, duration: float
) -> Callable[[int], float]:
  def _call(t: int) -> float:
    decay_steps = min(t, duration)
    return end_e + (start_e - end_e) * np.exp(-1.0 * decay_steps / duration)

  return _call

